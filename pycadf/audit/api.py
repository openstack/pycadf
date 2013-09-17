# -*- encoding: utf-8 -*-
#
# Copyright 2013 IBM Corp.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ast
import collections
import ConfigParser
import os
from oslo.config import cfg
import urlparse

from pycadf import cadftaxonomy as taxonomy
from pycadf import cadftype
from pycadf import credential
from pycadf import endpoint
from pycadf import eventfactory as factory
from pycadf import host
from pycadf import identifier
from pycadf import reason
from pycadf import reporterstep
from pycadf import resource
from pycadf import tag
from pycadf import timestamp

CONF = cfg.CONF
opts = [
    cfg.StrOpt('api_audit_map',
               default='api_audit_map.conf',
               help='File containing mapping for api paths and '
                    'service endpoints'),
]
CONF.register_opts(opts, group='audit')


class ClientResource(resource.Resource):
    def __init__(self, project_id=None, **kwargs):
        super(ClientResource, self).__init__(**kwargs)
        if project_id is not None:
            self.project_id = project_id


class KeystoneCredential(credential.Credential):
    def __init__(self, identity_status=None, **kwargs):
        super(KeystoneCredential, self).__init__(**kwargs)
        if identity_status is not None:
            self.identity_status = identity_status


class PycadfAuditApiConfigError(Exception):
    """Error raised when pyCADF fails to configure correctly."""


class OpenStackAuditApi(object):

    _API_PATHS = []
    _BODY_ACTIONS = {}
    _SERVICE_ENDPOINTS = {}

    Service = collections.namedtuple('Service',
                                     ['id', 'name', 'type', 'admin_endp',
                                     'public_endp', 'private_endp'])

    def __init__(self):
        self._configure_audit_map()

    def _configure_audit_map(self):
        """Configure to recognize and map known api paths."""

        cfg_file = CONF.audit.api_audit_map
        if not os.path.exists(CONF.audit.api_audit_map):
            cfg_file = cfg.CONF.find_file(CONF.audit.api_audit_map)

        if cfg_file:
            try:
                audit_map = ConfigParser.SafeConfigParser()
                audit_map.readfp(open(cfg_file))

                try:
                    paths = audit_map.get('DEFAULT', 'api_paths')
                    self._API_PATHS = paths.lstrip().split('\n')
                    self._DEFAULT_TARGET_ENDPOINT_TYPE = \
                        audit_map.get('DEFAULT', 'target_endpoint_type')
                except ConfigParser.NoSectionError:
                    pass

                try:
                    self._BODY_ACTIONS = dict(audit_map.items('body_actions'))
                except ConfigParser.NoSectionError:
                    pass

                try:
                    self._SERVICE_ENDPOINTS = \
                        dict(audit_map.items('service_endpoints'))
                except ConfigParser.NoSectionError:
                    pass
            except ConfigParser.ParsingError as err:
                raise PycadfAuditApiConfigError(
                    'Error parsing audit map file: %s' % err)

    def _get_action(self, req):
        """Take a given Request, parse url path to calculate action type.

        Depending on req.method:
        if POST: path ends with action, read the body and get action from map;
                 request ends with known path, assume is create action;
                 request ends with unknown path, assume is update action.
        if GET: request ends with known path, assume is list action;
                request ends with unknown path, assume is read action.
        if PUT, assume update action.
        if DELETE, assume delete action.
        if HEAD, assume read action.

        """
        path = urlparse.urlparse(req.url).path
        path = path[:-1] if path.endswith('/') else path

        method = req.method
        if method == 'POST':
            if path[path.rfind('/') + 1:] == 'action':
                if req.json:
                    body_action = req.json.keys()[0]
                    action = self._BODY_ACTIONS.get(body_action,
                                                    taxonomy.ACTION_CREATE)
                else:
                    action = taxonomy.ACTION_CREATE
            elif path[path.rfind('/') + 1:] not in self._API_PATHS:
                action = taxonomy.ACTION_UPDATE
            else:
                action = taxonomy.ACTION_CREATE
        elif method == 'GET':
            if path[path.rfind('/') + 1:] in self._API_PATHS:
                action = taxonomy.ACTION_LIST
            else:
                action = taxonomy.ACTION_READ
        elif method == 'PUT':
            action = taxonomy.ACTION_UPDATE
        elif method == 'DELETE':
            action = taxonomy.ACTION_DELETE
        elif method == 'HEAD':
            action = taxonomy.ACTION_READ
        else:
            action = taxonomy.UNKNOWN

        return action

    def _get_service_info(self, endp):
        service = self.Service(
            type=self._SERVICE_ENDPOINTS.get(
                endp['type'],
                taxonomy.UNKNOWN),
            name=endp['name'],
            id=endp['endpoints'][0]['id'],
            admin_endp=endpoint.Endpoint(
                name='admin',
                url=endp['endpoints'][0]['adminURL']),
            private_endp=endpoint.Endpoint(
                name='private',
                url=endp['endpoints'][0]['internalURL']),
            public_endp=endpoint.Endpoint(
                name='public',
                url=endp['endpoints'][0]['publicURL']))

        return service

    def create_event(self, req, correlation_id):
        action = self._get_action(req)
        initiator_host = host.Host(address=req.client_addr,
                                   agent=req.user_agent)
        catalog = ast.literal_eval(req.environ['HTTP_X_SERVICE_CATALOG'])
        service_info = self.Service(type=taxonomy.UNKNOWN,
                                    name=taxonomy.UNKNOWN,
                                    id=taxonomy.UNKNOWN,
                                    admin_endp=None,
                                    private_endp=None,
                                    public_endp=None)
        default_endpoint = None
        for endp in catalog:
            admin_urlparse = urlparse.urlparse(
                endp['endpoints'][0]['adminURL'])
            public_urlparse = urlparse.urlparse(
                endp['endpoints'][0]['publicURL'])
            req_url = urlparse.urlparse(req.host_url)
            if (req_url.netloc == admin_urlparse.netloc
                    or req_url.netloc == public_urlparse.netloc):
                service_info = self._get_service_info(endp)
                break
            elif (self._DEFAULT_TARGET_ENDPOINT_TYPE
                  and endp['type'] == self._DEFAULT_TARGET_ENDPOINT_TYPE):
                default_endpoint = endp
        else:
            if default_endpoint:
                service_info = self._get_service_info(default_endpoint)

        initiator = ClientResource(
            typeURI=taxonomy.ACCOUNT_USER,
            id=str(req.environ['HTTP_X_USER_ID']),
            name=req.environ['HTTP_X_USER_NAME'],
            host=initiator_host,
            credential=KeystoneCredential(
                token=req.environ['HTTP_X_AUTH_TOKEN'],
                identity_status=req.environ['HTTP_X_IDENTITY_STATUS']),
            project_id=req.environ['HTTP_X_PROJECT_ID'])
        target = resource.Resource(typeURI=service_info.type,
                                   id=service_info.id,
                                   name=service_info.name)
        if service_info.admin_endp:
            target.add_address(service_info.admin_endp)
        if service_info.private_endp:
            target.add_address(service_info.private_endp)
        if service_info.public_endp:
            target.add_address(service_info.public_endp)
        event = factory.EventFactory().new_event(
            eventType=cadftype.EVENTTYPE_ACTIVITY,
            outcome=taxonomy.OUTCOME_PENDING,
            action=action,
            initiator=initiator,
            target=target,
            observer='target')
        event.add_tag(tag.generate_name_value_tag('correlation_id',
                                                  correlation_id))
        return event

    def append_audit_event(self, req):
        """Append a CADF event to req.environ['CADF_EVENT']
        Also, stores model in request for future process and includes a
        CADF correlation id.
        """
        correlation_id = identifier.generate_uuid()
        req.environ['CADF_EVENT_CORRELATION_ID'] = correlation_id
        event = self.create_event(req, correlation_id)
        setattr(req, 'cadf_model', event)
        req.environ['CADF_EVENT'] = event.as_dict()

    def mod_audit_event(self, req, response):
        """Modifies CADF event in request based on response.
        If no event exists, a new event is created.
        """
        if response:
            if response.status_int >= 200 and response.status_int < 400:
                result = taxonomy.OUTCOME_SUCCESS
            else:
                result = taxonomy.OUTCOME_FAILURE
        else:
            result = taxonomy.UNKNOWN
        if hasattr(req, 'cadf_model'):
            req.cadf_model.add_reporterstep(
                reporterstep.Reporterstep(
                    role=cadftype.REPORTER_ROLE_MODIFIER,
                    reporter='target',
                    reporterTime=timestamp.get_utc_now()))
        else:
            self.append_audit_event(req)
        req.cadf_model.outcome = result
        if response:
            req.cadf_model.reason = \
                reason.Reason(reasonType='HTTP',
                              reasonCode=str(response.status_int))
        req.environ['CADF_EVENT'] = req.cadf_model.as_dict()
