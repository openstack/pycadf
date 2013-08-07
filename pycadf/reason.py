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

from pycadf import cadftype

TYPE_URI_REASON = cadftype.CADF_VERSION_1_0_0 + 'reason'

REASON_KEYNAME_REASONTYPE = "reasonType"
REASON_KEYNAME_REASONCODE = "reasonCode"
REASON_KEYNAME_POLICYTYPE = "policyType"
REASON_KEYNAME_POLICYID = "policyId"

REASON_KEYNAMES = [REASON_KEYNAME_REASONTYPE,
                   REASON_KEYNAME_REASONCODE,
                   REASON_KEYNAME_POLICYTYPE,
                   REASON_KEYNAME_POLICYID]


class Reason(cadftype.CADFAbstractType):

    reasonType = cadftype.ValidatorDescriptor(
        REASON_KEYNAME_REASONTYPE,
        lambda x: isinstance(x, basestring))
    reasonCode = cadftype.ValidatorDescriptor(
        REASON_KEYNAME_REASONCODE,
        lambda x: isinstance(x, basestring))
    policyType = cadftype.ValidatorDescriptor(
        REASON_KEYNAME_POLICYTYPE,
        lambda x: isinstance(x, basestring))
    policyId = cadftype.ValidatorDescriptor(
        REASON_KEYNAME_POLICYID,
        lambda x: isinstance(x, basestring))

    def __init__(self, reasonType=None, reasonCode=None, policyType=None,
                 policyId=None):

        # Reason.reasonType
        if reasonType is not None:
            setattr(self, REASON_KEYNAME_REASONTYPE, reasonType)

        # Reason.reasonCode
        if reasonCode is not None:
            setattr(self, REASON_KEYNAME_REASONCODE, reasonCode)

        # Reason.policyType
        if policyType is not None:
            setattr(self, REASON_KEYNAME_POLICYTYPE, policyType)

        # Reason.policyId
        if policyId is not None:
            setattr(self, REASON_KEYNAME_POLICYID, policyId)

    # TODO(mrutkows): validate this cadf:Reason type against schema
    def is_valid(self):
        # MUST have at least one valid pairing of reason+code or policy+id
        return ((hasattr(self, REASON_KEYNAME_REASONTYPE) and
                 hasattr(self, REASON_KEYNAME_REASONCODE)) or
                (hasattr(self, REASON_KEYNAME_POLICYTYPE) and
                 hasattr(self, REASON_KEYNAME_POLICYID)))
