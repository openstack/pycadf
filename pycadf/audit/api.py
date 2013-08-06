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
import ConfigParser
import os
from oslo.config import cfg
import urlparse

from pycadf import cadftaxonomy as taxonomy
from pycadf import cadftype
from pycadf import eventfactory as factory
from pycadf.openstack.common import log as logging
from pycadf import reason
from pycadf import reporterstep
from pycadf import resource
from pycadf import tag
from pycadf import timestamp

cfg.CONF.import_opt('api_audit_map', 'pycadf.audit', group='audit')

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class ServiceResource(resource.Resource):
    def __init__(self, admin_url=None, private_url=None,
                 public_url=None, **kwargs):
        super(ServiceResource, self).__init__(**kwargs)
        if admin_url is not None:
            self.adminURL = admin_url
        if private_url is not None:
            self.privateURL = private_url
        if public_url is not None:
            self.publicURL = public_url


class ClientResource(resource.Resource):
    def __init__(self, client_addr=None, user_agent=None,
                 token=None, tenant=None, status=None, **kwargs):
        super(ClientResource, self).__init__(**kwargs)
        if client_addr is not None:
            self.client_addr = client_addr
        if user_agent is not None:
            self.user_agent = user_agent
        if token is not None:
            self.token = token
        if tenant is not None:
            self.tenant = tenant
        if status is not None:
            self.status = status


class OpenStackAuditApi(object):

    _API_PATHS = []
    _BODY_ACTIONS = {}
    _SERVICE_ENDPOINTS = {}

    def __init__(self):
        self._configure_audit_map()

    def _configure_audit_map(self):
        """Configure to recognize and map known api paths."""

        cfg_file = CONF.audit.api_audit_map
        if not os.path.exists(CONF.audit.api_audit_map):
            cfg_file = cfg.CONF.find_file(CONF.audit.api_audit_map)
        LOG.debug("API path config file: %s", cfg_file)

        if cfg_file:
            try:
                audit_map = ConfigParser.SafeConfigParser()
                audit_map.readfp(open(cfg_file))

                try:
                    paths = audit_map.get('DEFAULT', 'api_paths')
                    self._API_PATHS = paths.lstrip().split('\n')
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
                LOG.error('Error parsing audit map file: %s' % err)

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

    def gen_event(self, req, correlation_id):
        action = self._get_action(req)
        catalog = ast.literal_eval(req.environ['HTTP_X_SERVICE_CATALOG'])
        for endpoint in catalog:
            admin_urlparse = urlparse.urlparse(
                endpoint['endpoints'][0]['adminURL'])
            public_urlparse = urlparse.urlparse(
                endpoint['endpoints'][0]['publicURL'])
            req_url = urlparse.urlparse(req.host_url)
            if (req_url.netloc == admin_urlparse.netloc
                    or req_url.netloc == public_urlparse.netloc):
                service_type = self._SERVICE_ENDPOINTS.get(endpoint['type'],
                                                           taxonomy.UNKNOWN)
                service_name = endpoint['name']
                admin_url = endpoint['endpoints'][0]['adminURL']
                private_url = endpoint['endpoints'][0]['internalURL']
                public_url = endpoint['endpoints'][0]['publicURL']
                service_id = endpoint['endpoints'][0]['id']
                break
        else:
            service_type = service_id = service_name = taxonomy.UNKNOWN
            admin_url = private_url = public_url = None

        event = factory.EventFactory().new_event(
            eventType=cadftype.EVENTTYPE_ACTIVITY,
            outcome=taxonomy.OUTCOME_PENDING,
            action=action,
            initiator=ClientResource(
                typeURI=taxonomy.ACCOUNT_USER,
                id=str(req.environ['HTTP_X_USER_ID']),
                name=req.environ['HTTP_X_USER_NAME'],
                client_addr=req.client_addr,
                user_agent=req.user_agent,
                token=req.environ['HTTP_X_AUTH_TOKEN'],
                tenant=req.environ['HTTP_X_PROJECT_ID'],
                status=req.environ['HTTP_X_IDENTITY_STATUS']),
            target=ServiceResource(typeURI=service_type,
                                   id=service_id,
                                   name=service_name,
                                   private_url=private_url,
                                   public_url=public_url,
                                   admin_url=admin_url))
        event.add_tag(tag.generate_name_value_tag('correlation_id',
                                                  correlation_id))
        return event

    def append_audit_event(self, msg, req, correlation_id):
        setattr(req, 'CADF_EVENT_CORRELATION_ID', correlation_id)
        event = self.gen_event(req, correlation_id)
        event.add_reporterstep(
            reporterstep.Reporterstep(
                role=cadftype.REPORTER_ROLE_OBSERVER,
                reporter='target'))
        msg['cadf_event'] = event

    def mod_audit_event(self, msg, response, correlation_id):
        if response.status_int >= 200 and response.status_int < 400:
            result = taxonomy.OUTCOME_SUCCESS
        else:
            result = taxonomy.OUTCOME_FAILURE
        if 'cadf_event' in msg:
            msg['cadf_event'].outcome = result
            msg['cadf_event'].reason = \
                reason.Reason(reasonType='HTTP',
                              reasonCode=str(response.status_int))
            msg['cadf_event'].add_reporterstep(
                reporterstep.Reporterstep(
                    role=cadftype.REPORTER_ROLE_MODIFIER,
                    reporter='target',
                    reporterTime=timestamp.get_utc_now()))
