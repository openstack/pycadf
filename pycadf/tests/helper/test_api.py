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

from pycadf import cadftaxonomy
from pycadf.helper import api
from pycadf.tests import base


class TestApiHelper(base.TestCase):
    def test_convert_req_action(self):
        self.assertEqual(cadftaxonomy.ACTION_READ,
                         api.convert_req_action('get'))
        self.assertEqual(cadftaxonomy.ACTION_CREATE,
                         api.convert_req_action('POST'))
        self.assertEqual(cadftaxonomy.ACTION_DELETE,
                         api.convert_req_action('deLetE'))

    def test_convert_req_action_invalid(self):
        self.assertEqual(cadftaxonomy.UNKNOWN, api.convert_req_action(124))
        self.assertEqual(cadftaxonomy.UNKNOWN, api.convert_req_action('blah'))

    def test_convert_req_action_with_details(self):
        detail = 'compute/instance'
        self.assertEqual(cadftaxonomy.ACTION_READ + '/%s' % detail,
                         api.convert_req_action('GET', detail))
        self.assertEqual(cadftaxonomy.ACTION_DELETE + '/%s' % detail,
                         api.convert_req_action('DELETE', detail))

    def test_convert_req_action_with_details_invalid(self):
        detail = 123
        self.assertEqual(cadftaxonomy.ACTION_READ,
                         api.convert_req_action('GET', detail))
        self.assertEqual(cadftaxonomy.ACTION_DELETE,
                         api.convert_req_action('DELETE', detail))
