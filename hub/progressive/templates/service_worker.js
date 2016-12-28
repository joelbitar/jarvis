{% load static %}
{% load version_tags %}
/**
 * Created by joel on 2016-12-20.
 */
var CACHE_NAME = 'jarvis-v{% real_version_number %}';
var urlsToCache = [
    '/',
    '{% static "css/angular-material.min.css" %}',
    '{% static "css/device.css" %}',
    '{% static "css/jarvis.css" %}',

    '{% static "fonts/weather-icons/css/weather-icons.min.css" %}',

    '{% static "js/startpage.js" %}',
    '{% static "js/angularjs/angular.min.js" %}',
    '{% static "js/angularjs/i18n/angular-locale_sv-se.js" %}',
    '{% static "js/angularjs/angular-animate.min.js" %}',
    '{% static "js/angularjs/angular-aria.min.js" %}',
    '{% static "js/angularjs/angular-route.min.js" %}',
    '{% static "js/angularjs/angular-cookies.min.js" %}',

    '{% static "js/lib/ngStorage.min.js" %}',
    '{% static "js/focus.js" %}',

    '{% static "js/lib/lodash.min.js" %}',
    '{% static "js/lib/visibly.js" %}',
    '{% static "js/lib/loading-bar.js" %}',
    '{% static "js/lib/restangular.min.js" %}',

    '{% static "js/angular-material.min.js" %}',

    '{% static "js/app.js" %}',

    '{% static "js/startpage.js" %}',
    '{% static "js/admin.js" %}',

    '{% static "js/device.js" %}',
    '{% static "js/node.js" %}',
    '{% static "js/devicegroup.js" %}',
    '{% static "js/sensor.js" %}',
    '{% static "js/weather.js" %}',
    '{% static "js/login.js" %}',
    '{% static "js/signals.js" %}',

    '{% static "ng-templates/startpage.html" %}',

    '{% static "ng-templates/device-detail.html" %}',
    '{% static "ng-templates/device-group-teaser.html" %}',
    '{% static "ng-templates/device-teaser.html" %}',

    '{% static "ng-templates/directive/weather-icon.html" %}',
    '{% static "ng-templates/forecast-teaser.html" %}',
    '{% static "ng-templates/weather.html" %}',

    '{% static "ng-templates/sensor-detail.html" %}',
    '{% static "ng-templates/sensor-teaser.html" %}'
];

self.addEventListener('install', function(event) {
    // Perform install steps
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});
