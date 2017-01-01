from django.test import TestCase
from django.test import Client

# Create your tests here.

class HTMLIndexTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_to_root_should_return_index(self):
        r = self.client.get('/')

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertEqual(
            r.template_name,
            ['index.html']
        )

    # Because AngularJS HTML5 routing
    def test_request_to_device_should_return_index(self):
        r = self.client.get('/device/1/')

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertEqual(
            r.template_name,
            ['index.html']
        )

    def test_request_to_other_paths_should_return_index(self):
        for path in ('/administration/recent-signals/', '/administration/node/1/commands/test-path/'):
            r = self.client.get(path)

            self.assertEqual(
                r.status_code,
                200,
                'Did NOT return 200 ok when trying to fetch for path: ' + path
            )

            self.assertEqual(
                r.template_name,
                ['index.html'],
                'Did NOT return index template when trying to fetch for path: ' + path
            )
