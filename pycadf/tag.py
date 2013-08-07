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


def generate_name_value_tag(name, value):
    # TODO(mrutkows): detailed test/concatenation of independent values
    # into a URI
    if name is None or value is None:
        raise ValueError('Invalid name and/or value. Values cannot be None')

    tag = name + "?value=" + value
    return tag


# TODO(mrutkows): validate any Tag's name?value= format
def is_valid(value):
    if not isinstance(value, basestring):
        raise TypeError
    return True
