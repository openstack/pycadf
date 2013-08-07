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

import uuid

from pycadf import cadftype
from pycadf import timestamp


# TODO(mrutkows): Add openstack namespace prefix (e.g. 'openstack:') to all
# cadf:Identifiers
# TODO(mrutkows): make the namespace prefix configurable and have it resolve to
# a full openstack namespace/domain value via some declaration (e.g.
# "openstack:" == "http:\\www.openstack.org\")...
def generate_uuid():
    uuid_temp = uuid.uuid5(uuid.NAMESPACE_DNS,
                           cadftype.CADF_VERSION_1_0_0
                           + timestamp.get_utc_now())
    return str(uuid_temp)


# TODO(mrutkows): validate any cadf:Identifier (type) record against
# CADF schema.  This would include schema validation as an optional parm.
def is_valid(value):
    if not isinstance(value, basestring):
        raise TypeError
    return True
