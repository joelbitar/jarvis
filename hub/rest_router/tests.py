import json
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup
import re


# Create your tests here.
class DjangoSettingsTestsBase(TestCase):
    def helper_get_client_side_django_settings(self):
        c = Client()

        r = c.get('/')
        soup = BeautifulSoup(r.content, 'html.parser')

        settings_script_elm = soup.find(id="settings")

        content = "".join([l.strip(' ') for l in settings_script_elm.get_text().split('\n')])

        match = re.match('var\s\w*\s=\s(.*);', content)

        self.assertIsNotNone(
            match
        )

        json.loads(match.groups()[0])

        j = json.loads(match.groups()[0])

        return j


class DjangoRestRouterSettings(DjangoSettingsTestsBase):
    def test_should_have_rest_router_in_client_settings_if_hub_url_is_something_in_settings(self):
        settings.MAIN_HUB_URL = 'http://example.com'

        d = self.helper_get_client_side_django_settings()

        u = reverse('hub-proxy').lstrip('/')

        self.assertEqual(
            d['proxy_url'],
            u
        )

    def test_should_have_none_as_proxy_url_if_none_is_set_in_settings(self):
        settings.MAIN_HUB_URL = None

        d = self.helper_get_client_side_django_settings()

        self.assertEqual(
            d['proxy_url'],
            ''
        )


class HttpProxyTests(TestCase):
    def test_should_get_pretty_json_error_when_no_backend_available(self):
        settings.TEST_MODE = False
        settings.MAIN_HUB_URL = 'http://127.0.0.1:9090/nothihng/'

        c = Client()

        r = c.get(
            reverse('hub-proxy', kwargs={
                'path': 'auth/current/'
            })
        )

        self.assertEqual(
            r.status_code,
            502
        )

        self.assertJSONEqual(
            r.content.decode('utf-8'),
            json.dumps(
                {
                    'error': 'connection-error',
                    'message': 'Could not connect to main hub',
                }
            )
        )




