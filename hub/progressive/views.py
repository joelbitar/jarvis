from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.views.generic import TemplateView
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
            "background_color": "#FAFAFA",
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
            ),
            (
                "logo-192.png",
                "192"
            ),
            (
                "logo-256.png",
                "256"
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


class ServiceWorkerView(TemplateView):
    template_name = 'service_worker.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        context['non_versioned_resources'] = (
            "img/xs_light_on.png",
            "img/xs_light_off.png",
            "img/light_on.png",
            "img/light_off.png",
            "images/icons/menu.svg",

            "fonts/weather-icons/font/WeatherIcons-Regular.otf",
            "fonts/weather-icons/font/weathericons-regular-webfont.eot",
            "fonts/weather-icons/font/weathericons-regular-webfont.svg",
            "fonts/weather-icons/font/weathericons-regular-webfont.ttf",
            "fonts/weather-icons/font/weathericons-regular-webfont.woff",
            "fonts/weather-icons/font/weathericons-regular-webfont.woff2"
        )

        context['resources'] = (
            "css/angular-material.min.css",
            "css/device.css",
            "css/jarvis.css",

            "images/logo/logo.png",
            "images/logo/logo-180.png",
            "images/logo/logo-192.png",
            "images/logo/logo-256.png",

            "fonts/weather-icons/css/weather-icons.min.css",
            "fonts/weather-icons/css/weather-icons-wind.min.css",

            "images/icons/ic_autorenew_black_24px.svg",
            "images/icons/ic_autorenew_white_24px.svg",

            "js/angularjs/angular.min.js",
            "js/angularjs/i18n/angular-locale_sv-se.js",
            "js/angularjs/angular-animate.min.js",
            "js/angularjs/angular-aria.min.js",
            "js/angularjs/angular-cookies.min.js",
            "js/angularjs/angular-messages.min.js",
            "js/angularjs/angular-resource.min.js",
            "js/angularjs/angular-route.min.js",
            "js/angularjs/angular-touch.min.js",

            "js/lib/ngStorage.min.js",
            "js/focus.js",

            "js/lib/highcharts.js",
            "js/lib/lodash.min.js",
            "js/lib/visibly.js",
            "js/lib/loading-bar.min.js",
            "css/loading-bar.min.css",
            "js/lib/restangular.min.js",
            "js/lib/moment.js",

            "js/angular-material.min.js",

            "js/app.js",

            "js/startpage.js",
            "js/admin.js",

            "js/device.js",
            "js/node.js",
            "js/devicegroup.js",
            "js/sensor.js",
            "js/weather.js",
            "js/login.js",
            "js/signals.js",

            "ng-templates/startpage.html",
            "ng-templates/login.html",

            "ng-templates/admin/index.html",
            "ng-templates/admin/recent-signals.html",

            "ng-templates/device-detail.html",
            "ng-templates/device-group-teaser.html",
            "ng-templates/device-teaser.html",

            "ng-templates/directive/weather-icon.html",
            "ng-templates/directive/wind-icon.html",
            "ng-templates/forecast-teaser.html",
            "ng-templates/weather.html",

            "ng-templates/sensor-detail.html",
            "ng-templates/sensor-teaser.html"
        )

        return context
