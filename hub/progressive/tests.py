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

        self.assertJSONEqual(
            r.content.decode('utf-8'),
            json.dumps(
            {
                "short_name": "YARVIS",
                "name": "Yet Another Rather Very Intelligent System",
                "display" : "standalone",
                "theme_color": "#673AB7",
                "icons": [
                    {
                        "src": static("images/logo/logo.png"),
                        "type": "image/png",
                        "sizes": "64x64"
                    },
                    {
                        "src": static("images/logo/logo-180.png"),
                        "type": "image/png",
                        "sizes": "180x180"
                    }
                ],
                "start_url": "/"
            })
        )
