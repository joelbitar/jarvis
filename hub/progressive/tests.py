from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
import json

# Create your tests here.

class ManifestJSONTests(TestCase):
    def test_get_manifest_json(self):
        c = Client()
        r = c.get(
            reverse('manifest-json')
        )

        self.assertEqual(
            r.status_code,
            200
        )

        # Will throw error if not valid json
        j = json.loads(r.content.decode('utf-8'))

        self.assertEqual(
            j["short_name"],
            "YARVIS"
        )

        self.assertTrue(
            len(j["icons"]) > 0
        )
