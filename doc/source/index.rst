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

===============================
 PyCADF developer documentation
===============================

The `CADF (Cloud Audit Data Federation Working Group)`_ is working to develop
open standards for audit data which can be federated from cloud providers,
with the intent to elevate customer's trust in cloud hosted applications.

Specifications and profiles produced by the CADF will help protect the
investments of companies seeking to move their applications to cloud
deployment models and preserve their ability to audit operational processes,
regardless of their chosen cloud provider. The CADF develops specifications
for audit event data and interface models and a compatible interaction model
that will describe interactions between IT resources for cloud deployment models.

pyCADF is the python implementation of the CADF specification. This documentation
offers information on how CADF works and how to contribute to the project.

.. _CADF (Cloud Audit Data Federation Working Group): http://www.dmtf.org/standards/cadf

Getting Started
===============

.. toctree::
    :maxdepth: 1

    event_concept
    specification/index
    middleware
    audit_maps

Contributing
============

pyCADF utilizes all of the usual OpenStack processes and requirements for
contributions. The code is hosted `on OpenStack's Git server`_. `Bug reports`_
and `blueprints`_ may be submitted to the :code:`pycadf` project on
`Launchpad`_.  Code may be submitted to the :code:`openstack/pycadf` project
using `Gerrit`_.

.. _`on OpenStack's Git server`: https://git.openstack.org/cgit/openstack/pycadf/tree
.. _Launchpad: https://launchpad.net/pycadf
.. _Gerrit: http://docs.openstack.org/infra/manual/developers.html#development-workflow
.. _Bug reports: https://bugs.launchpad.net/pycadf/+bugs
.. _blueprints: https://blueprints.launchpad.net/pycadf
.. _PyPi: https://pypi.python.org/pypi/pycadf
.. _tarball: http://tarballs.openstack.org/pycadf

Code Documentation
==================
.. toctree::
   :maxdepth: 1

   api/modules

Release Notes
=============

.. toctree::
   :maxdepth: 1

   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
