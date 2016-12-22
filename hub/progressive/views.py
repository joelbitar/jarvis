from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.staticfiles.templatetags.staticfiles import static

class ManifestView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        manifest = {
            "short_name": "YARVIS",
            "name": "Yet Another Rather Very Intelligent System",
            "display" : "standalone",
            "theme_color": "#673AB7",
            "icons": [],
            "start_url": "/"
        }

        manifest_icons = (
            (
                "logo.png",
                "64"
            ),
            (
                "logo-180.png",
                "180"
            )
        )
        for image_name, size in manifest_icons:
            manifest['icons'].append(
                {
                    "src": static("images/logo/" + image_name),
                    "type": "image/png",
                    "sizes": size + "x" + size
                }
            )

        return Response(
            manifest
        )

