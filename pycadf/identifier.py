# Copyright 2013 IBM Corp.
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
import hashlib
import uuid
import warnings

from debtcollector import removals
from oslo_config import cfg
import six

CONF = cfg.CONF
opts = [
    cfg.StrOpt('namespace',
               default='openstack',
               help='namespace prefix for generated id'),
]
CONF.register_opts(opts, group='audit')


AUDIT_NS = None
if CONF.audit.namespace:
    md5_hash = hashlib.md5(CONF.audit.namespace.encode('utf-8'))
    AUDIT_NS = uuid.UUID(md5_hash.hexdigest())


def generate_uuid():
    """Generate a CADF identifier."""
    if AUDIT_NS:
        return str(uuid.uuid5(AUDIT_NS, str(uuid.uuid4())))
    return str(uuid.uuid4())


@removals.remove
def norm_ns(str_id):
    """Apply a namespace to the identifier."""
    prefix = CONF.audit.namespace + ':' if CONF.audit.namespace else ''
    return prefix + str_id


def is_valid(value):
    """Validation to ensure Identifier is correct."""
    if value in ['target', 'initiator', 'observer']:
        return True
    try:
        uuid.UUID(value)
    except (ValueError, TypeError):
        if not isinstance(value, six.string_types) or not value:
            return False
        warnings.warn('Invalid uuid. To ensure interoperability, identifiers'
                      'should be a valid uuid.')
    return True
