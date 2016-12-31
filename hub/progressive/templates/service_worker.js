{% load static %}{% load version_tags %}var CACHE_NAME = "jarvis-{% version_number %}", urlsToCache = [
    '/',

    '{% static "css/angular-material.min.css" %}{% version_extension %}',
    '{% static "css/device.css" %}{% version_extension %}',
    '{% static "css/jarvis.css" %}{% version_extension %}',

    '{% static "fonts/weather-icons/css/weather-icons.min.css" %}{% version_extension %}',

    '{% static "images/icons/ic_autorenew_black_24px.svg" %}',
    '{% static "images/icons/ic_autorenew_white_24px.svg" %}',
    '{% static "img/xs_light_on.png" %}',
    '{% static "img/xs_light_off.png" %}',
    '{% static "images/icons/menu.svg" %}',

    '{% static "js/angularjs/angular.min.js" %}{% version_extension %}',
    '{% static "js/angularjs/i18n/angular-locale_sv-se.js" %}{% version_extension %}',
    '{% static "js/angularjs/angular-animate.min.js" %}{% version_extension %}',
    '{% static "js/angularjs/angular-aria.min.js" %}{% version_extension %}',
    '{% static "js/angularjs/angular-route.min.js" %}{% version_extension %}',
    '{% static "js/angularjs/angular-cookies.min.js" %}{% version_extension %}',

    '{% static "js/lib/ngStorage.min.js" %}{% version_extension %}',
    '{% static "js/focus.js" %}{% version_extension %}',

    '{% static "js/lib/lodash.min.js" %}{% version_extension %}',
    '{% static "js/lib/visibly.js" %}{% version_extension %}',
    '{% static "js/lib/loading-bar.js" %}{% version_extension %}',
    '{% static "js/lib/restangular.min.js" %}{% version_extension %}',

    '{% static "js/angular-material.min.js" %}{% version_extension %}',

    '{% static "js/app.js" %}{% version_extension %}',

    '{% static "js/startpage.js" %}{% version_extension %}',
    '{% static "js/admin.js" %}{% version_extension %}',

    '{% static "js/device.js" %}{% version_extension %}',
    '{% static "js/node.js" %}{% version_extension %}',
    '{% static "js/devicegroup.js" %}{% version_extension %}',
    '{% static "js/sensor.js" %}{% version_extension %}',
    '{% static "js/weather.js" %}{% version_extension %}',
    '{% static "js/login.js" %}{% version_extension %}',
    '{% static "js/signals.js" %}{% version_extension %}',

    '{% static "ng-templates/startpage.html" %}{% version_extension %}',

    '{% static "ng-templates/device-detail.html" %}{% version_extension %}',
    '{% static "ng-templates/device-group-teaser.html" %}{% version_extension %}',
    '{% static "ng-templates/device-teaser.html" %}{% version_extension %}',

    '{% static "ng-templates/directive/weather-icon.html" %}{% version_extension %}',
    '{% static "ng-templates/forecast-teaser.html" %}{% version_extension %}',
    '{% static "ng-templates/weather.html" %}{% version_extension %}',

    '{% static "ng-templates/sensor-detail.html" %}{% version_extension %}',
    '{% static "ng-templates/sensor-teaser.html" %}{% version_extension %}'
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

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.match(event.request).then(function (response) {
        return response || fetch(event.request).then(function(response) {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    })
  );
});
