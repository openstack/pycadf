# -*- encoding: utf-8 -*-
#
# Copyright 2013 IBM Corp.
#
# Author: Matt Rutkowski <mrutkows@us.ibm.com>
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

from pycadf import attachment
from pycadf import cadftaxonomy
from pycadf import cadftype
from pycadf import identifier
from pycadf import measurement
from pycadf import reason
from pycadf import reporterstep
from pycadf import resource
from pycadf import tag
from pycadf import timestamp

TYPE_URI_EVENT = cadftype.CADF_VERSION_1_0_0 + 'event'

# Event.eventType
EVENT_KEYNAME_TYPEURI = "typeURI"
EVENT_KEYNAME_EVENTTYPE = "eventType"
EVENT_KEYNAME_ID = "id"
EVENT_KEYNAME_EVENTTIME = "eventTime"
EVENT_KEYNAME_INITIATOR = "initiator"
EVENT_KEYNAME_INITIATORID = "initiatorId"
EVENT_KEYNAME_ACTION = "action"
EVENT_KEYNAME_TARGET = "target"
EVENT_KEYNAME_TARGETID = "targetId"
EVENT_KEYNAME_OUTCOME = "outcome"
EVENT_KEYNAME_REASON = "reason"
EVENT_KEYNAME_SEVERITY = "severity"
EVENT_KEYNAME_MEASUREMENTS = "measurements"
EVENT_KEYNAME_TAGS = "tags"
EVENT_KEYNAME_ATTACHMENTS = "attachments"
EVENT_KEYNAME_OBSERVER = "observer"
EVENT_KEYNAME_REPORTERCHAIN = "reporterchain"

EVENT_KEYNAMES = [EVENT_KEYNAME_TYPEURI,
                  EVENT_KEYNAME_EVENTTYPE,
                  EVENT_KEYNAME_ID,
                  EVENT_KEYNAME_EVENTTIME,
                  EVENT_KEYNAME_INITIATOR,
                  EVENT_KEYNAME_INITIATORID,
                  EVENT_KEYNAME_ACTION,
                  EVENT_KEYNAME_TARGET,
                  EVENT_KEYNAME_TARGETID,
                  EVENT_KEYNAME_OUTCOME,
                  EVENT_KEYNAME_REASON,
                  EVENT_KEYNAME_SEVERITY,
                  EVENT_KEYNAME_MEASUREMENTS,
                  EVENT_KEYNAME_TAGS,
                  EVENT_KEYNAME_ATTACHMENTS,
                  EVENT_KEYNAME_OBSERVER,
                  EVENT_KEYNAME_REPORTERCHAIN]


class Event(cadftype.CADFAbstractType):

    eventType = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_EVENTTYPE, lambda x: cadftype.is_valid_eventType(x))
    id = cadftype.ValidatorDescriptor(EVENT_KEYNAME_ID,
                                      lambda x: identifier.is_valid(x))
    eventTime = cadftype.ValidatorDescriptor(EVENT_KEYNAME_EVENTTIME,
                                             lambda x: timestamp.is_valid(x))
    initiator = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_INITIATOR,
        (lambda x: isinstance(x, resource.Resource) and
         x.is_valid()))
    initiatorId = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_INITIATORID, lambda x: identifier.is_valid(x))
    action = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_ACTION, lambda x: cadftaxonomy.is_valid_action(x))
    target = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_TARGET, (lambda x: isinstance(x, resource.Resource) and
                               x.is_valid()))
    targetId = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_TARGETID, lambda x: identifier.is_valid(x))
    outcome = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_OUTCOME, lambda x: cadftaxonomy.is_valid_outcome(x))
    reason = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_REASON,
        lambda x: isinstance(x, reason.Reason) and x.is_valid())
    severity = cadftype.ValidatorDescriptor(EVENT_KEYNAME_SEVERITY,
                                            lambda x: isinstance(x,
                                                                 basestring))
    observer = cadftype.ValidatorDescriptor(
        EVENT_KEYNAME_OBSERVER,
        (lambda x: isinstance(x, resource.Resource) or
         (isinstance(x, basestring) and
          (x == 'initiator' or x == 'target'))))

    def __init__(self, eventType=cadftype.EVENTTYPE_ACTIVITY,
                 id=identifier.generate_uuid(),
                 eventTime=timestamp.get_utc_now(),
                 action=cadftaxonomy.UNKNOWN, outcome=cadftaxonomy.UNKNOWN,
                 initiator=None, initiatorId=None, target=None, targetId=None,
                 severity=None, reason=None, observer=None):

        # Establish typeURI for the CADF Event data type
        # TODO(mrutkows): support extended typeURIs for Event subtypes
        setattr(self, EVENT_KEYNAME_TYPEURI, TYPE_URI_EVENT)

        # Event.eventType (Mandatory)
        setattr(self, EVENT_KEYNAME_EVENTTYPE, eventType)

        # Event.id (Mandatory)
        setattr(self, EVENT_KEYNAME_ID, id)

        # Event.eventTime (Mandatory)
        setattr(self, EVENT_KEYNAME_EVENTTIME, eventTime)

        # Event.action (Mandatory)
        setattr(self, EVENT_KEYNAME_ACTION, action)

        # Event.outcome (Mandatory)
        setattr(self, EVENT_KEYNAME_OUTCOME, outcome)

        # Event.observer (Mandatory)
        setattr(self, EVENT_KEYNAME_OBSERVER, observer)

        # Event.initiator (Mandatory if no initiatorId)
        if initiator is not None:
            setattr(self, EVENT_KEYNAME_INITIATOR, initiator)

        # Event.initiatorId (Dependent)
        if initiatorId is not None:
            setattr(self, EVENT_KEYNAME_INITIATORID, initiatorId)

        # Event.target (Mandatory if no targetId)
        if target is not None:
            setattr(self, EVENT_KEYNAME_TARGET, target)

        # Event.targetId (Dependent)
        if targetId is not None:
            setattr(self, EVENT_KEYNAME_TARGETID, targetId)

        # Event.severity (Optional)
        if severity is not None:
            setattr(self, EVENT_KEYNAME_SEVERITY, severity)

        # Event.reason (Optional)
        if reason is not None:
            setattr(self, EVENT_KEYNAME_REASON, reason)

    # Event.reporterchain
    def add_reporterstep(self, step):
        if step is not None and isinstance(step, reporterstep.Reporterstep):
            if step.is_valid():
                # Create the list of Reportersteps if needed
                if not hasattr(self, EVENT_KEYNAME_REPORTERCHAIN):
                    setattr(self, EVENT_KEYNAME_REPORTERCHAIN, list())

                reporterchain = getattr(self,
                                        EVENT_KEYNAME_REPORTERCHAIN)
                reporterchain.append(step)
            else:
                raise ValueError('Invalid reporterstep')
        else:
            raise ValueError('Invalid reporterstep. '
                             'Value must be a Reporterstep')

    # Event.measurements
    def add_measurement(self, measure_val):
        if (measure_val is not None
                and isinstance(measure_val, measurement.Measurement)):

            if measure_val.is_valid():

                # Create the list of event.Measurements if needed
                if not hasattr(self, EVENT_KEYNAME_MEASUREMENTS):
                    setattr(self, EVENT_KEYNAME_MEASUREMENTS, list())

                measurements = getattr(self, EVENT_KEYNAME_MEASUREMENTS)
                measurements.append(measure_val)
            else:
                raise ValueError('Invalid measurement')
        else:
            raise ValueError('Invalid measurement. '
                             'Value must be a Measurement')

    # Event.tags
    def add_tag(self, tag_val):
        if tag.is_valid(tag_val):
            if not hasattr(self, EVENT_KEYNAME_TAGS):
                setattr(self, EVENT_KEYNAME_TAGS, list())
            getattr(self, EVENT_KEYNAME_TAGS).append(tag_val)
        else:
            raise ValueError('Invalid tag')

    # Event.attachments
    def add_attachment(self, attachment_val):
        if (attachment_val is not None
                and isinstance(attachment_val, attachment.Attachment)):

            if attachment_val.is_valid():
                # Create the list of Attachments if needed
                if not hasattr(self, EVENT_KEYNAME_ATTACHMENTS):
                    setattr(self, EVENT_KEYNAME_ATTACHMENTS, list())

                attachments = getattr(self, EVENT_KEYNAME_ATTACHMENTS)
                attachments.append(attachment_val)
            else:
                raise ValueError('Invalid attachment')
        else:
            raise ValueError('Invalid attachment. '
                             'Value must be an Attachment')

    # self validate cadf:Event record against schema
    def is_valid(self):
        # TODO(mrutkows): Eventually, make sure all attributes are
        # from either the CADF spec. (or profiles thereof)
        # TODO(mrutkows): validate all child attributes that are CADF types
        # TODO(mrutkows): Cannot have both an initiator and initiatorId
        # TODO(mrutkows): Cannot have both an target and targetId
        return (
            hasattr(self, EVENT_KEYNAME_TYPEURI) and
            hasattr(self, EVENT_KEYNAME_EVENTTYPE) and
            hasattr(self, EVENT_KEYNAME_ID) and
            hasattr(self, EVENT_KEYNAME_EVENTTIME) and
            hasattr(self, EVENT_KEYNAME_ACTION) and
            hasattr(self, EVENT_KEYNAME_OUTCOME) and
            hasattr(self, EVENT_KEYNAME_INITIATOR) and
            hasattr(self, EVENT_KEYNAME_TARGET)
        )
