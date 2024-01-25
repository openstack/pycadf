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
import re
import uuid
import warnings

from oslo_config import cfg

CONF = cfg.CONF
opts = [
    cfg.StrOpt('namespace',
               default='openstack',
               help='namespace prefix for generated id'),
]
CONF.register_opts(opts, group='audit')


AUDIT_NS = None
if CONF.audit.namespace:
    sha256_hash = hashlib.sha256(CONF.audit.namespace.encode('utf-8'))
    AUDIT_NS = uuid.UUID(sha256_hash.hexdigest()[0:32])

VALID_EXCEPTIONS = ['default', 'initiator', 'observer', 'target']


def generate_uuid():
    """Generate a CADF identifier."""
    if AUDIT_NS:
        return str(uuid.uuid5(AUDIT_NS, str(uuid.uuid4())))
    return str(uuid.uuid4())


def _check_valid_uuid(value):
    """Checks a value for one or multiple valid uuids joined together."""

    if not value:
        raise ValueError

    value = re.sub('[{}-]|urn:uuid:', '', value)
    for val in [value[i:i + 32] for i in range(0, len(value), 32)]:
        uuid.UUID(val)


def is_valid(value):
    """Validation to ensure Identifier is correct.

    If the Identifier value is a string type but not a valid UUID string,
    warn against interoperability issues and return True. This relaxes
    the requirement of having strict UUID checking.
    """
    if value in VALID_EXCEPTIONS:
        return True
    try:
        _check_valid_uuid(value)
    except (ValueError, TypeError):
        if not isinstance(value, str) or not value:
            return False
        warnings.warn(('Invalid uuid: %s. To ensure interoperability, '
                      'identifiers should be a valid uuid.' % (value)))
    return True
