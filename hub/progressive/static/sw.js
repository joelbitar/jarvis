/**
 * Created by joel on 2016-12-20.
 */
var CACHE_NAME = 'jarvis-v1.1';
var urlsToCache = [
    '/',
    'css/angular-material.min.css',
    'css/device.css',
    'css/jarvis.css',

    'fonts/weather-icons/css/weather-icons.min.css',

    'js/startpage.js',
    'js/angularjs/angular.min.js',
    'js/angularjs/i18n/angular-locale_sv-se.js',
    'js/angularjs/angular-animate.min.js',
    'js/angularjs/angular-aria.min.js',
    'js/angularjs/angular-route.min.js',
    'js/angularjs/angular-cookies.min.js',

    'js/lib/ngStorage.min.js',
    'js/focus.js',

    'js/lib/lodash.min.js',
    'js/lib/restangular.min.js',

    'js/angular-material.min.js',

    'js/startpage.js',
    'js/device.js',
    'js/node.js',
    'js/devicegroup.js',
    'js/sensor.js',
    'js/weather.js',
    'js/login.js',
    'js/signals.js',

    'ng-templates/device-detail.html',
    'ng-templates/device-group-teaser.html',
    'ng-templates/device-teaser.html',

    'ng-templates/directive/weather-icon.html',
    'ng-templates/forecast-teaser.html',
    'ng-templates/weather.html',

    'ng-templates/sensor-detail.html',
    'ng-templates/sensor-teaser.html'
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
