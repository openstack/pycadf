# Copyright 2013 OpenStack LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import time
from unittest import mock
import uuid

from pycadf import attachment
from pycadf import cadftype
from pycadf import credential
from pycadf import endpoint
from pycadf import event
from pycadf import geolocation
from pycadf import host
from pycadf import identifier
from pycadf import measurement
from pycadf import metric
from pycadf import reason
from pycadf import reporterstep
from pycadf import resource
from pycadf import tag
from pycadf.tests import base
from pycadf import timestamp


class TestCADFSpec(base.TestCase):

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_generated_uuid(self, warning_mock):
        # generated uuid
        self.assertTrue(identifier.is_valid(identifier.generate_uuid()))
        self.assertFalse(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_empty_string_is_invalid(self, warning_mock):
        # empty string
        self.assertFalse(identifier.is_valid(''))
        self.assertFalse(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_any_string_is_invalid(self, warning_mock):
        # any string
        self.assertTrue(identifier.is_valid('blah'))
        self.assertTrue(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_joined_uuids_are_valid(self, warning_mock):
        # multiple uuids joined together
        long_128_uuids = [
            ('3adce28e67e44544a5a9d5f1ab54f578a86d310aac3a465e9d'
             'd2693a78b45c0e42dce28e67e44544a5a9d5f1ab54f578a86d'
             '310aac3a465e9dd2693a78b45c0e'),
            ('{3adce28e67e44544a5a9d5f1ab54f578a86d310aac3a465e9d'
             'd2693a78b45c0e42dce28e67e44544a5a9d5f1ab54f578a86d'
             '310aac3a465e9dd2693a78b45c0e}'),
            ('{12345678-1234-5678-1234-567812345678'
             '12345678-1234-5678-1234-567812345678'
             '12345678-1234-5678-1234-567812345678'
             '12345678-1234-5678-1234-567812345678}'),
            ('urn:uuid:3adce28e67e44544a5a9d5f1ab54f578a86d310aac3a465e9d'
             'd2693a78b45c0e42dce28e67e44544a5a9d5f1ab54f578a86d'
             '310aac3a465e9dd2693a78b45c0e')]

        for value in long_128_uuids:
            self.assertTrue(identifier.is_valid(value))
            self.assertFalse(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_long_nonjoined_uuid_is_invalid(self, warning_mock):
        # long uuid not of size % 32
        char_42_id = '3adce28e67e44544a5a9d5f1ab54f578a86d310aac'
        self.assertTrue(identifier.is_valid(char_42_id))
        self.assertTrue(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_specific_exceptions_are_valid(self, warning_mock):
        # uuid exceptions
        for value in identifier.VALID_EXCEPTIONS:
            self.assertTrue(identifier.is_valid(value))
            self.assertFalse(warning_mock.called)

    @mock.patch('pycadf.identifier.warnings.warn')
    def test_identifier_valid_id_extra_chars_is_valid(self, warning_mock):
        # valid uuid with additional characters according to:
        # https://docs.python.org/2/library/uuid.html
        valid_ids = [
            '{1234567890abcdef1234567890abcdef}',
            '{12345678-1234-5678-1234-567812345678}',
            'urn:uuid:12345678-1234-5678-1234-567812345678']

        for value in valid_ids:
            self.assertTrue(identifier.is_valid(value))
            self.assertFalse(warning_mock.called)

    def test_endpoint(self):
        endp = endpoint.Endpoint(url='http://192.168.0.1',
                                 name='endpoint name',
                                 port='8080')
        self.assertEqual(True, endp.is_valid())
        dict_endp = endp.as_dict()
        for key in endpoint.ENDPOINT_KEYNAMES:
            self.assertIn(key, dict_endp)

    def test_host(self):
        h = host.Host(id=identifier.generate_uuid(),
                      address='192.168.0.1',
                      agent='client',
                      platform='AIX')
        self.assertEqual(True, h.is_valid())
        dict_host = h.as_dict()
        for key in host.HOST_KEYNAMES:
            self.assertIn(key, dict_host)

    def test_credential(self):
        cred = credential.Credential(type='auth token',
                                     token=identifier.generate_uuid())
        self.assertEqual(True, cred.is_valid())
        dict_cred = cred.as_dict()
        for key in credential.CRED_KEYNAMES:
            self.assertIn(key, dict_cred)

    def test_federated_credential(self):
        cred = credential.FederatedCredential(
            token=identifier.generate_uuid(),
            type='http://docs.oasis-open.org/security/saml/v2.0',
            identity_provider=identifier.generate_uuid(),
            user=identifier.generate_uuid(),
            groups=[
                identifier.generate_uuid(),
                identifier.generate_uuid(),
                identifier.generate_uuid()])
        self.assertEqual(True, cred.is_valid())
        dict_cred = cred.as_dict()
        for key in credential.FED_CRED_KEYNAMES:
            self.assertIn(key, dict_cred)

    def test_geolocation(self):
        geo = geolocation.Geolocation(id=identifier.generate_uuid(),
                                      latitude='43.6481 N',
                                      longitude='79.4042 W',
                                      elevation='0',
                                      accuracy='1',
                                      city='toronto',
                                      state='ontario',
                                      regionICANN='ca')
        self.assertEqual(True, geo.is_valid())

        dict_geo = geo.as_dict()
        for key in geolocation.GEO_KEYNAMES:
            self.assertIn(key, dict_geo)

    def test_metric(self):
        metric_val = metric.Metric(metricId=identifier.generate_uuid(),
                                   unit='b',
                                   name='bytes')
        self.assertEqual(True, metric_val.is_valid())

        dict_metric_val = metric_val.as_dict()
        for key in metric.METRIC_KEYNAMES:
            self.assertIn(key, dict_metric_val)

    def test_measurement(self):
        measure_val = measurement.Measurement(
            result='100',
            metric=metric.Metric(),
            metricId=identifier.generate_uuid(),
            calculatedBy=resource.Resource(typeURI='storage'))
        self.assertEqual(False, measure_val.is_valid())

        dict_measure_val = measure_val.as_dict()
        for key in measurement.MEASUREMENT_KEYNAMES:
            self.assertIn(key, dict_measure_val)

        measure_val = measurement.Measurement(
            result='100',
            metric=metric.Metric(),
            calculatedBy=resource.Resource(typeURI='storage'))
        self.assertEqual(True, measure_val.is_valid())

        measure_val = measurement.Measurement(
            result='100',
            metricId=identifier.generate_uuid(),
            calculatedBy=resource.Resource(typeURI='storage'))
        self.assertEqual(True, measure_val.is_valid())

    def test_reason(self):
        reason_val = reason.Reason(reasonType='HTTP',
                                   reasonCode='200',
                                   policyType='poltype',
                                   policyId=identifier.generate_uuid())
        self.assertEqual(True, reason_val.is_valid())

        dict_reason_val = reason_val.as_dict()
        for key in reason.REASON_KEYNAMES:
            self.assertIn(key, dict_reason_val)

    def test_reporterstep(self):
        step = reporterstep.Reporterstep(
            role='modifier',
            reporter=resource.Resource(typeURI='storage'),
            reporterId=identifier.generate_uuid(),
            reporterTime=timestamp.get_utc_now())
        self.assertEqual(False, step.is_valid())

        dict_step = step.as_dict()
        for key in reporterstep.REPORTERSTEP_KEYNAMES:
            self.assertIn(key, dict_step)

        step = reporterstep.Reporterstep(
            role='modifier',
            reporter=resource.Resource(typeURI='storage'),
            reporterTime=timestamp.get_utc_now())
        self.assertEqual(True, step.is_valid())

        step = reporterstep.Reporterstep(
            role='modifier',
            reporterId=identifier.generate_uuid(),
            reporterTime=timestamp.get_utc_now())
        self.assertEqual(True, step.is_valid())

    def test_attachment(self):
        attach = attachment.Attachment(typeURI='attachURI',
                                       content='content',
                                       name='attachment_name')
        self.assertEqual(True, attach.is_valid())

        dict_attach = attach.as_dict()
        for key in attachment.ATTACHMENT_KEYNAMES:
            self.assertIn(key, dict_attach)

    def test_resource(self):
        res = resource.Resource(typeURI='storage',
                                name='res_name',
                                domain='res_domain',
                                ref='res_ref',
                                credential=credential.Credential(
                                    token=identifier.generate_uuid()),
                                host=host.Host(address='192.168.0.1'),
                                geolocation=geolocation.Geolocation(),
                                geolocationId=identifier.generate_uuid())

        res.add_attachment(attachment.Attachment(typeURI='attachURI',
                                                 content='content',
                                                 name='attachment_name'))
        res.add_address(endpoint.Endpoint(url='http://192.168.0.1'))

        self.assertEqual(True, res.is_valid())
        dict_res = res.as_dict()
        for key in resource.RESOURCE_KEYNAMES:
            self.assertIn(key, dict_res)

    def test_resource_shortform(self):
        res = resource.Resource(id='target')
        self.assertEqual(True, res.is_valid())

        res.add_attachment(attachment.Attachment(typeURI='attachURI',
                                                 content='content',
                                                 name='attachment_name'))
        self.assertEqual(False, res.is_valid())

    def test_event(self):
        ev = event.Event(eventType='activity',
                         id=identifier.generate_uuid(),
                         eventTime=timestamp.get_utc_now(),
                         initiator=resource.Resource(typeURI='storage'),
                         initiatorId=identifier.generate_uuid(),
                         action='read',
                         target=resource.Resource(typeURI='storage'),
                         targetId=identifier.generate_uuid(),
                         observer=resource.Resource(id='target'),
                         observerId=identifier.generate_uuid(),
                         outcome='success',
                         reason=reason.Reason(reasonType='HTTP',
                                              reasonCode='200'),
                         severity='high',
                         name='descriptive name')
        ev.add_measurement(
            measurement.Measurement(result='100',
                                    metricId=identifier.generate_uuid())),
        ev.add_tag(tag.generate_name_value_tag('name', 'val'))
        ev.add_attachment(attachment.Attachment(typeURI='attachURI',
                                                content='content',
                                                name='attachment_name'))
        ev.observer = resource.Resource(typeURI='service/security')
        ev.add_reporterstep(reporterstep.Reporterstep(
            role='observer',
            reporter=resource.Resource(typeURI='service/security')))
        ev.add_reporterstep(reporterstep.Reporterstep(
            reporterId=identifier.generate_uuid()))
        self.assertEqual(False, ev.is_valid())

        dict_ev = ev.as_dict()
        for key in event.EVENT_KEYNAMES:
            self.assertIn(key, dict_ev)

        ev = event.Event(eventType='activity',
                         id=identifier.generate_uuid(),
                         eventTime=timestamp.get_utc_now(),
                         initiator=resource.Resource(typeURI='storage'),
                         action='read',
                         target=resource.Resource(typeURI='storage'),
                         observer=resource.Resource(id='target'),
                         outcome='success')
        self.assertEqual(True, ev.is_valid())

        ev = event.Event(eventType='activity',
                         id=identifier.generate_uuid(),
                         eventTime=timestamp.get_utc_now(),
                         initiatorId=identifier.generate_uuid(),
                         action='read',
                         targetId=identifier.generate_uuid(),
                         observerId=identifier.generate_uuid(),
                         outcome='success')
        self.assertEqual(True, ev.is_valid())

        ev = event.Event(eventType='activity',
                         id=identifier.generate_uuid(),
                         eventTime=timestamp.get_utc_now(),
                         initiator=resource.Resource(typeURI='storage'),
                         action='read',
                         targetId=identifier.generate_uuid(),
                         observer=resource.Resource(id='target'),
                         outcome='success')
        self.assertEqual(True, ev.is_valid())

    def test_event_unique(self):
        ev = event.Event(eventType='activity',
                         initiator=resource.Resource(typeURI='storage'),
                         action='read',
                         target=resource.Resource(typeURI='storage'),
                         observer=resource.Resource(id='target'),
                         outcome='success')
        time.sleep(1)
        ev2 = event.Event(eventType='activity',
                          initiator=resource.Resource(typeURI='storage'),
                          action='read',
                          target=resource.Resource(typeURI='storage'),
                          observer=resource.Resource(id='target'),
                          outcome='success')
        self.assertNotEqual(ev.id, ev2.id)
        self.assertNotEqual(ev.eventTime, ev2.eventTime)

    def test_event_resource_shortform_not_self(self):
        self.assertRaises(ValueError,
                          lambda: event.Event(
                              eventType='activity',
                              initiator=resource.Resource(typeURI='storage'),
                              action='read',
                              target=resource.Resource(id='target'),
                              observer=resource.Resource(id='target'),
                              outcome='success'))
        self.assertRaises(ValueError,
                          lambda: event.Event(
                              eventType='activity',
                              initiator=resource.Resource(id='initiator'),
                              action='read',
                              target=resource.Resource(typeURI='storage'),
                              observer=resource.Resource(id='target'),
                              outcome='success'))

    def _create_none_validator_descriptor(self):
        class Owner(object):
            x = cadftype.ValidatorDescriptor(uuid.uuid4().hex)

        owner = Owner()
        owner.x = None

    def test_invalid_value_descriptor(self):
        """Test setting a ValidatorDescriptor to None results in ValueError"""

        self.assertRaises(ValueError, self._create_none_validator_descriptor)

    def test_cadfabstracttype_attribute_error(self):
        """Test an invalid CADFAbstractType attribute is set returns False"""

        h = host.Host(id=identifier.generate_uuid(),
                      address='192.168.0.1',
                      agent='client',
                      platform='AIX')
        self.assertEqual(False, h._isset(uuid.uuid4().hex))
