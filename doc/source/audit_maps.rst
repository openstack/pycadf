..
      Copyright 2014 IBM Corp.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

.. _audit_maps:

============
 Audit maps
============

The pyCADF library maintains a set of audit mapping files for OpenStack
services. Currently, pyCADF supplies the following audit mapping files:

* `cinder_api_audit_map.conf`_
* `glance_api_audit_map.conf`_
* `neutron_api_audit_map.conf`_
* `nova_api_audit_map.conf`_
* `trove_api_audit_map.conf`_
* `heat_api_audit_map.conf`_
* `ironic_api_audit_map.conf`_

These files are hosted under the `etc/pycadf`_ directory of pyCADF. For more
information on how to use these mapping files, refer to the `Audit middleware`_
section of the `keystonemiddleware`_ project.

.. _Audit middleware: http://docs.openstack.org/developer/keystonemiddleware/audit.html
.. _keystonemiddleware: http://docs.openstack.org/developer/keystonemiddleware
.. _`etc/pycadf`: https://github.com/openstack/pycadf/tree/master/etc/pycadf
.. _`cinder_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/cinder_api_audit_map.conf
.. _`glance_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/glance_api_audit_map.conf
.. _`neutron_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/neutron_api_audit_map.conf
.. _`nova_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/nova_api_audit_map.conf
.. _`trove_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/trove_api_audit_map.conf
.. _`heat_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/heat_api_audit_map.conf
.. _`ironic_api_audit_map.conf`: https://github.com/openstack/pycadf/blob/master/etc/pycadf/ironic_api_audit_map.conf
