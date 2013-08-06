#
# Copyright 2013 OpenStack LLC
# All Rights Reserved
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
import testtools

from pycadf import attachment
from pycadf import event
from pycadf import geolocation
from pycadf import identifier
from pycadf import measurement
from pycadf import metric
from pycadf import reason
from pycadf import reporterstep
from pycadf import resource
from pycadf import tag
from pycadf import timestamp


class TestCADFSpec(testtools.TestCase):
    def test_geolocation(self):
        geo = geolocation.Geolocation(id=identifier.generate_uuid(),
                                      latitude='43.6481 N',
                                      longitude='79.4042 W',
                                      elevation='0',
                                      accuracy='1',
                                      city='toronto',
                                      state='ontario',
                                      regionICANN='ca')

        dict_geo = geo.as_dict()
        for key in geolocation.GEO_KEYNAMES:
            self.assertIn(key, dict_geo)

    def test_metric(self):
        metric_val = metric.Metric(metricId=identifier.generate_uuid(),
                                   unit='b',
                                   name='bytes')

        dict_metric_val = metric_val.as_dict()
        for key in metric.METRIC_KEYNAMES:
            self.assertIn(key, dict_metric_val)

    def test_measurement(self):
        measure_val = measurement.Measurement(
            result='100',
            metric=metric.Metric(),
            metricId=identifier.generate_uuid(),
            calculatedBy=resource.Resource(typeURI='storage'))

        dict_measure_val = measure_val.as_dict()
        for key in measurement.MEASUREMENT_KEYNAMES:
            self.assertIn(key, dict_measure_val)

    def test_reason(self):
        reason_val = reason.Reason(reasonType='HTTP',
                                   reasonCode='200',
                                   policyType='poltype',
                                   policyId=identifier.generate_uuid())

        dict_reason_val = reason_val.as_dict()
        for key in reason.REASON_KEYNAMES:
            self.assertIn(key, dict_reason_val)

    def test_reporterstep(self):
        step = reporterstep.Reporterstep(
            role='observer',
            reporter=resource.Resource(typeURI='storage'),
            reporterId=identifier.generate_uuid(),
            reporterTime=timestamp.get_utc_now())

        dict_step = step.as_dict()
        for key in reporterstep.REPORTERSTEP_KEYNAMES:
            self.assertIn(key, dict_step)

    def test_attachment(self):
        attach = attachment.Attachment(typeURI='attachURI',
                                       content='content',
                                       name='attachment_name')

        dict_attach = attach.as_dict()
        for key in attachment.ATTACHMENT_KEYNAMES:
            self.assertIn(key, dict_attach)

    def test_resource(self):
        res = resource.Resource(typeURI='storage',
                                name='res_name',
                                domain='res_domain',
                                ref='res_ref',
                                geolocation=geolocation.Geolocation(),
                                geolocationId=identifier.generate_uuid())

        res.add_attachment(attachment.Attachment(typeURI='attachURI',
                                                 content='content',
                                                 name='attachment_name'))
        dict_res = res.as_dict()
        for key in resource.RESOURCE_KEYNAMES:
            self.assertIn(key, dict_res)

    def test_event(self):
        ev = event.Event(eventType='activity',
                         id=identifier.generate_uuid(),
                         eventTime=timestamp.get_utc_now(),
                         initiator=resource.Resource(typeURI='storage'),
                         initiatorId=identifier.generate_uuid(),
                         action='read',
                         target=resource.Resource(typeURI='storage'),
                         targetId=identifier.generate_uuid(),
                         outcome='success',
                         reason=reason.Reason(reasonType='HTTP',
                                              reasonCode='200'),
                         severity='high')
        ev.add_measurement(measurement.Measurement(result='100'))
        ev.add_tag(tag.generate_name_value_tag('name', 'val'))
        ev.add_attachment(attachment.Attachment(typeURI='attachURI',
                                                content='content',
                                                name='attachment_name'))
        ev.add_reporterstep(reporterstep.Reporterstep(
            role='observer',
            reporterId=identifier.generate_uuid()))

        dict_ev = ev.as_dict()
        for key in event.EVENT_KEYNAMES:
            self.assertIn(key, dict_ev)
