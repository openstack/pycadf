=============
Release Notes
=============

0.7.0 (Date TBD)
================

* Work toward Python 3.4 support and testing
* Use oslo_debug_helper and remove our own version
* Stop using intersphinx
* Remove dependencies from docs test env in tox.ini
* Use correct name of oslo debugger script
* Remove unused dependencies from pycadf
* Use oslo tests fixture
* Use oslo.serialization
* Sync oslo libraries
* Bug 1336976_: PyCADF docs do not include the changelog

.. _1336976: https://bugs.launchpad.net/pycadf/+bug/1336976

0.6.0 (Aug 23 2014)
===================

* Bump hacking to 0.9.2 series
* Remove docutils pin
* Enabled hacking checks H305 and H307
* Fix typo comments
* Fix a grammatical error in contributing doc
* Debug env for tox
* clean up license headers
* add CONTRIBUTING doc
* revise readme with a project description
* Enable PEP8 checks E128, E251 and E265
* define the project goal
* Blueprint audit-all-apis_: add audit support for all openstack components
* Bug 1359495_: Federated credential metadata

.. _audit-all-apis: https://blueprints.launchpad.net/pycadf/+spec/audit-all-apis
.. _1359495: https://bugs.launchpad.net/pycadf/+bug/1359495

0.5.1 (May 26 2014)
===================

* import run_cross_tests.sh from incubator
* reorder documentation
* sync oslo
* Bug 1321080_: [OSSA 2014-021] auth token is exposed in meter http.request (CVE-2014-4615)

.. _1321080: https://bugs.launchpad.net/pycadf/+bug/1321080

0.5 (Apr 1 2014)
================

* add docstrings to functions
* Bug 1279951_: need to publish developer documentation

.. _1279951: https://bugs.launchpad.net/pycadf/+bug/1279951

0.4.1 (Feb 21 2014)
===================

* catch empty json body

0.4 (Feb 20 2014)
=================

* Update .gitreview after repo rename
* Install configs into /etc, not /usr/etc
* Rollback change to that Install configs into /etc
* oslo common code sync and requirements cleanup
* add constant for security service
* Bug 1280327_: notifier middleware broken by oslo.messaging

.. _1280327: https://bugs.launchpad.net/pycadf/+bug/1280327

0.3.1 (Feb 4 2014)
==================

* update audit_map
* update build_typeURI to drop query string
* sync common code and requirements
* adjust typeURI to capture target better
* Python 3: update setup.cfg to advertise python 3 compatibility
* Bug 1262393_: mask token values
* Bug 1267500_: add REST request URL path to event

.. _1262393: https://bugs.launchpad.net/pycadf/+bug/1262393
.. _1267500: https://bugs.launchpad.net/pycadf/+bug/1267500

0.3 (Jan 10 2014)
=================

* Python 3: do not index a dict_keys object
* Python 3: use six.moves.urllib.parse instead of urlparse
* Python 3: the request body should be bytes in test_api.py
* Python 3: use six.with_metaclass
* Python 3: replace 'basestring' by 'six.string_types'
* Python 3: Use six.moves.configparser rather than ConfigParser
* sync requirements and oslo

0.2.2 (Oct 29 2013)
===================

* update oslo requirement
* do not set typeURI in resource shortform
* add namespace to all ids
* improve model validation

0.2.1 (Oct 21 2013)
===================

* support namespace prefix in id
* switch list action to read/list
* Bug 1240067_: observer should be implemented as resource

.. _1240067: https://bugs.launchpad.net/pycadf/+bug/1240067

0.2 (Oct 4 2013)
================

* Bug 1229977_: Switch to oslo.config 1.2.0 final
* Bug 1226870_: target_endpoint_type conf value not tested properly
* Bug 1228199_: conf options are not optional

.. _1229977: https://bugs.launchpad.net/pycadf/+bug/1229977
.. _1226870: https://bugs.launchpad.net/pycadf/+bug/1226870
.. _1228199: https://bugs.launchpad.net/pycadf/+bug/1228199

0.1.9 (Sep 19 2013)
===================

* Bug 1227634_: pycadf 0.1.8 broke oslo

.. _1227634: https://bugs.launchpad.net/pycadf/+bug/1227634

0.1.8 (Sep 18 2013)
===================

* update tox to 1.6
* Bug 1226722_: DNS names may not map to service catalog values

.. _1226722: https://bugs.launchpad.net/pycadf/+bug/1226722

0.1.7 (Sep 5 2013)
==================

* Bug 1221379_: Ceilometer CADF_EVENT.id and CADF_EVENT.eventTime stay the
  same for two different events

.. _1221379: https://bugs.launchpad.net/pycadf/+bug/1221379

0.1.6 (Sep 4 2013)
===================

* bump oslo.config req to 1.2.0a3

0.1.5 (Aug 26 2013)
===================

* Bug 1214097_: update cadf spec to support new data model

  * support credentials, hosts, endpoints
  * add observer attr to event

* Bug 1214407_: api_audit_map.conf is not getting packaged

.. _1214097: https://bugs.launchpad.net/pycadf/+bug/1214097
.. _1214407: https://bugs.launchpad.net/pycadf/+bug/1214407

0.1.4 (Aug 20 2013)
===================

* add event to CADF_EVENT

0.1.3 (Aug 15 2013)
===================

* add support for no response and failed request audit

0.1.2 (Aug 14 2013)
===================

* move cadf correlation id under req.environ
* append cadf event to req.environ
* Bug 1209387_: attribute validation fails against unicode

.. _1209387: https://bugs.launchpad.net/pycadf/+bug/1209387

0.1.1 (Aug 8 2013)
==================

* validate attributes against basestring
* add support for audit api middleware

0.1 (Aug 6 2013)
================

* initial project setup