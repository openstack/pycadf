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

from pycadf import cadftype

TYPE_URI_ACTION = cadftype.CADF_VERSION_1_0_0 + 'action'

UNKNOWN = 'unknown'

# Commonly used (valid) Event.action values from Nova
ACTION_CREATE = 'create'
ACTION_READ = 'read'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'
# Other CADF actions
ACTION_AUTHENTICATE = 'authenticate'
ACTION_EVALUATE = 'evaluate'
# OpenStack specific, Profile or change CADF spec. to add this action
ACTION_LIST = 'read/list'

# TODO(mrutkows): Make global using WSGI mechanism
ACTION_TAXONOMY = frozenset([
    'backup',
    'capture',
    ACTION_CREATE,
    'configure',
    ACTION_READ,
    ACTION_LIST,
    ACTION_UPDATE,
    ACTION_DELETE,
    'monitor',
    'start',
    'stop',
    'deploy',
    'undeploy',
    'enable',
    'disable',
    'send',
    'receive',
    ACTION_AUTHENTICATE,
    'authenticate/login',
    'revoke',
    'renew',
    'restore',
    ACTION_EVALUATE,
    'allow',
    'deny',
    'notify',
    UNKNOWN
])


# TODO(mrutkows): validate absolute URIs as well
def is_valid_action(value):
    for type in ACTION_TAXONOMY:
        if value.startswith(type):
            return True
    return False


TYPE_URI_OUTCOME = cadftype.CADF_VERSION_1_0_0 + 'outcome'

# Valid Event.outcome values
OUTCOME_SUCCESS = 'success'
OUTCOME_FAILURE = 'failure'
OUTCOME_PENDING = 'pending'

# TODO(mrutkows): Make global using WSGI mechanism
OUTCOME_TAXONOMY = frozenset([
    OUTCOME_SUCCESS,
    OUTCOME_FAILURE,
    OUTCOME_PENDING,
    UNKNOWN
])


# TODO(mrutkows): validate absolute URIs as well
def is_valid_outcome(value):
    return value in OUTCOME_TAXONOMY

SERVICE_SECURITY = 'service/security'
SERVICE_KEYMGR = 'service/security/keymanager'
ACCOUNT_USER = 'service/security/account/user'
CADF_AUDIT_FILTER = 'service/security/audit/filter'

SECURITY_ACCOUNT = 'data/security/account'
SECURITY_CREDENTIAL = 'data/security/credential'
SECURITY_DOMAIN = 'data/security/domain'
SECURITY_ENDPOINT = 'data/security/endpoint'
SECURITY_GROUP = 'data/security/group'
SECURITY_IDENTITY = 'data/security/identity'
SECURITY_KEY = 'data/security/key'
SECURITY_LICENCE = 'data/security/license'
SECURITY_POLICY = 'data/security/policy'
SECURITY_PROFILE = 'data/security/profile'
SECURITY_PROJECT = 'data/security/project'
SECURITY_REGION = 'data/security/region'
SECURITY_ROLE = 'data/security/role'
SECURITY_SERVICE = 'data/security/service'
SECURITY_TRUST = 'data/security/trust'
SECURITY_ACCOUNT_USER = 'data/security/account/user'
KEYMGR_SECRET = 'data/security/keymanager/secret'
KEYMGR_CONTAINER = 'data/security/keymanager/container'
KEYMGR_ORDER = 'data/security/keymanager/order'
KEYMGR_OTHERS = 'data/security/keymanager'


# TODO(mrutkows): Make global using WSGI mechanism
RESOURCE_TAXONOMY = frozenset([
    'storage',
    'storage/node',
    'storage/volume',
    'storage/memory',
    'storage/container',
    'storage/directory',
    'storage/database',
    'storage/queue',
    'compute',
    'compute/node',
    'compute/cpu',
    'compute/machine',
    'compute/process',
    'compute/thread',
    'network',
    'network/node',
    'network/node/host',
    'network/connection',
    'network/domain',
    'network/cluster',
    'service',
    'service/oss',
    'service/bss',
    'service/bss/metering',
    'service/composition',
    'service/compute',
    'service/database',
    SERVICE_SECURITY,
    SERVICE_KEYMGR,
    'service/security/account',
    ACCOUNT_USER,
    CADF_AUDIT_FILTER,
    'service/storage',
    'service/storage/block',
    'service/storage/image',
    'service/storage/object',
    'service/network',
    'data',
    'data/message',
    'data/workload',
    'data/workload/app',
    'data/workload/service',
    'data/workload/task',
    'data/workload/job',
    'data/file',
    'data/file/catalog',
    'data/file/log',
    'data/template',
    'data/package',
    'data/image',
    'data/module',
    'data/config',
    'data/directory',
    'data/database',
    'data/security',
    SECURITY_ACCOUNT,
    SECURITY_CREDENTIAL,
    SECURITY_DOMAIN,
    SECURITY_ENDPOINT,
    SECURITY_GROUP,
    SECURITY_IDENTITY,
    SECURITY_KEY,
    SECURITY_LICENCE,
    SECURITY_POLICY,
    SECURITY_PROFILE,
    SECURITY_PROJECT,
    SECURITY_REGION,
    SECURITY_ROLE,
    SECURITY_SERVICE,
    SECURITY_TRUST,
    SECURITY_ACCOUNT_USER,
    'data/security/account/user/privilege',
    'data/database/alias',
    'data/database/catalog',
    'data/database/constraints',
    'data/database/index',
    'data/database/instance',
    'data/database/key',
    'data/database/routine',
    'data/database/schema',
    'data/database/sequence',
    'data/database/table',
    'data/database/trigger',
    'data/database/view',
    KEYMGR_CONTAINER,
    KEYMGR_ORDER,
    KEYMGR_SECRET,
    KEYMGR_OTHERS,
    UNKNOWN
])


# TODO(mrutkows): validate absolute URIs as well
def is_valid_resource(value):
    for type in RESOURCE_TAXONOMY:
        if value.startswith(type):
            return True
    return False
