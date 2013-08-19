# -*- encoding: utf-8 -*-
#
# Copyright © 2013 IBM Corporation
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
from pycadf import identifier

TYPE_URI_HOST = cadftype.CADF_VERSION_1_0_0 + 'host'

HOST_KEYNAME_ID = "id"
HOST_KEYNAME_ADDR = "address"
HOST_KEYNAME_AGENT = "agent"
HOST_KEYNAME_PLATFORM = "platform"

HOST_KEYNAMES = [HOST_KEYNAME_ID,
                 HOST_KEYNAME_ADDR,
                 HOST_KEYNAME_AGENT,
                 HOST_KEYNAME_PLATFORM]


class Host(cadftype.CADFAbstractType):

    id = cadftype.ValidatorDescriptor(
        HOST_KEYNAME_ID, lambda x: identifier.is_valid(x))
    address = cadftype.ValidatorDescriptor(
        HOST_KEYNAME_ADDR, lambda x: isinstance(x, basestring))
    agent = cadftype.ValidatorDescriptor(
        HOST_KEYNAME_AGENT, lambda x: isinstance(x, basestring))
    platform = cadftype.ValidatorDescriptor(
        HOST_KEYNAME_PLATFORM, lambda x: isinstance(x, basestring))

    def __init__(self, id=None, address=None, agent=None,
                 platform=None):

        # Host.id
        if id is not None:
            setattr(self, HOST_KEYNAME_ID, id)
        # Host.address
        if address is not None:
            setattr(self, HOST_KEYNAME_ADDR, address)
        # Host.agent
        if agent is not None:
            setattr(self, HOST_KEYNAME_AGENT, agent)
        # Host.platform
        if platform is not None:
            setattr(self, HOST_KEYNAME_PLATFORM, platform)

    # TODO(mrutkows): validate this cadf:Host type against schema
    def is_valid(self):
        return (hasattr(self, HOST_KEYNAME_ID) or
                hasattr(self, HOST_KEYNAME_ADDR) or
                hasattr(self, HOST_KEYNAME_AGENT) or
                hasattr(self, HOST_KEYNAME_PLATFORM))
