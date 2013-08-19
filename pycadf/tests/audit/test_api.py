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
from oslo.config import cfg
import uuid
import webob

from pycadf.audit import api
from pycadf.tests import base


class TestAuditApi(base.TestCase):
    ENV_HEADERS = {'HTTP_X_SERVICE_CATALOG':
                   '''[{"endpoints_links": [],
                        "endpoints": [{"adminURL":
                                       "http://host:8774/v2/admin",
                                       "region": "RegionOne",
                                       "publicURL":
                                       "http://host:8774/v2/public",
                                       "internalURL":
                                       "http://host:8774/v2/internal",
                                       "id": "resource_id"}],
                        "type": "compute",
                        "name": "nova"},]''',
                   'HTTP_X_USER_ID': 'user_id',
                   'HTTP_X_USER_NAME': 'user_name',
                   'HTTP_X_AUTH_TOKEN': 'token',
                   'HTTP_X_PROJECT_ID': 'tenant_id',
                   'HTTP_X_IDENTITY_STATUS': 'Confirmed'}

    def setUp(self):
        super(TestAuditApi, self).setUp()
        # set nova CONF.host value
        # Set a default location for the api_audit_map config file
        cfg.CONF.set_override(
            'api_audit_map',
            self.path_get('etc/pycadf/api_audit_map.conf'),
            group='audit'
        )
        self.audit_api = api.OpenStackAuditApi()

    def api_request(self, method, url):
        self.ENV_HEADERS['REQUEST_METHOD'] = method
        req = webob.Request.blank(url, environ=self.ENV_HEADERS,
                                  remote_addr='192.168.0.1')
        self.audit_api.append_audit_event(req)
        self.assertIn('CADF_EVENT_CORRELATION_ID', req.environ)
        return req

    def test_get_list(self):
        req = self.api_request('GET', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'list')
        self.assertEqual(payload['typeURI'],
                         'http://schemas.dmtf.org/cloud/audit/1.0/event')
        self.assertEqual(payload['outcome'], 'pending')
        self.assertEqual(payload['eventType'], 'activity')
        self.assertEqual(payload['target']['name'], 'nova')
        self.assertEqual(payload['target']['id'], 'resource_id')
        self.assertEqual(payload['target']['typeURI'], 'service/compute')
        self.assertEqual(len(payload['target']['addresses']), 3)
        self.assertEqual(payload['target']['addresses'][0]['name'], 'admin')
        self.assertEqual(payload['target']['addresses'][0]['url'],
                         'http://host:8774/v2/admin')
        self.assertEqual(payload['initiator']['id'], 'user_id')
        self.assertEqual(payload['initiator']['name'], 'user_name')
        self.assertEqual(payload['initiator']['project_id'], 'tenant_id')
        self.assertEqual(payload['initiator']['host']['address'],
                         '192.168.0.1')
        self.assertEqual(payload['initiator']['typeURI'],
                         'service/security/account/user')
        self.assertEqual(payload['initiator']['credential']['token'], 'token')
        self.assertEqual(payload['initiator']['credential']['identity_status'],
                         'Confirmed')
        self.assertNotIn('reason', payload)
        self.assertNotIn('reporterchain', payload)
        self.assertEqual(payload['observer'], 'target')

    def test_get_read(self):
        req = self.api_request('GET',
                               'http://host:8774/v2/public/servers/' +
                               str(uuid.uuid4()))
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'read')
        self.assertEqual(payload['outcome'], 'pending')

    def test_get_unknown_endpoint(self):
        req = self.api_request('GET',
                               'http://unknown:8774/v2/public/servers/')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'list')
        self.assertEqual(payload['outcome'], 'pending')
        self.assertEqual(payload['target']['name'], 'unknown')
        self.assertEqual(payload['target']['id'], 'unknown')
        self.assertEqual(payload['target']['typeURI'], 'unknown')

    def test_put(self):
        req = self.api_request('PUT', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'update')
        self.assertEqual(payload['outcome'], 'pending')

    def test_delete(self):
        req = self.api_request('DELETE', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'delete')
        self.assertEqual(payload['outcome'], 'pending')

    def test_head(self):
        req = self.api_request('HEAD', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'read')
        self.assertEqual(payload['outcome'], 'pending')

    def test_post_update(self):
        req = self.api_request('POST',
                               'http://host:8774/v2/public/servers/' +
                               str(uuid.uuid4()))
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'update')
        self.assertEqual(payload['outcome'], 'pending')

    def test_post_create(self):
        req = self.api_request('POST', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'create')
        self.assertEqual(payload['outcome'], 'pending')

    def test_post_action(self):
        self.ENV_HEADERS['REQUEST_METHOD'] = 'POST'
        req = webob.Request.blank('http://host:8774/v2/public/servers/action',
                                  environ=self.ENV_HEADERS)
        req.body = '{"createImage" : {"name" : "new-image","metadata": ' \
                   '{"ImageType": "Gold","ImageVersion": "2.0"}}}'
        self.audit_api.append_audit_event(req)
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['action'], 'create')
        self.assertEqual(payload['outcome'], 'pending')

    def test_response_mod_msg(self):
        req = self.api_request('GET', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.audit_api.mod_audit_event(req, webob.Response())
        payload2 = req.environ['CADF_EVENT']
        self.assertEqual(payload['id'], payload2['id'])
        self.assertEqual(payload['tags'], payload2['tags'])
        self.assertEqual(payload2['outcome'], 'success')
        self.assertEqual(payload2['reason']['reasonType'], 'HTTP')
        self.assertEqual(payload2['reason']['reasonCode'], '200')
        self.assertEqual(len(payload2['reporterchain']), 1)
        self.assertEqual(payload2['reporterchain'][0]['role'], 'modifier')
        self.assertEqual(payload2['reporterchain'][0]['reporter'], 'target')

    def test_no_response(self):
        req = self.api_request('GET', 'http://host:8774/v2/public/servers')
        payload = req.environ['CADF_EVENT']
        self.audit_api.mod_audit_event(req, None)
        payload2 = req.environ['CADF_EVENT']
        self.assertEqual(payload['id'], payload2['id'])
        self.assertEqual(payload['tags'], payload2['tags'])
        self.assertEqual(payload2['outcome'], 'unknown')
        self.assertNotIn('reason', payload2)
        self.assertEqual(len(payload2['reporterchain']), 1)
        self.assertEqual(payload2['reporterchain'][0]['role'], 'modifier')
        self.assertEqual(payload2['reporterchain'][0]['reporter'], 'target')

    def test_missing_req(self):
        self.ENV_HEADERS['REQUEST_METHOD'] = 'GET'
        req = webob.Request.blank('http://host:8774/v2/public/servers',
                                  environ=self.ENV_HEADERS)
        self.assertNotIn('CADF_EVENT', req.environ)
        self.audit_api.mod_audit_event(req, webob.Response())
        self.assertIn('CADF_EVENT', req.environ)
        self.assertIn('CADF_EVENT_CORRELATION_ID', req.environ)
        payload = req.environ['CADF_EVENT']
        self.assertEqual(payload['outcome'], 'success')
        self.assertEqual(payload['reason']['reasonType'], 'HTTP')
        self.assertEqual(payload['reason']['reasonCode'], '200')
        self.assertEqual(payload['observer'], 'target')
        self.assertNotIn('reporterchain', payload)
