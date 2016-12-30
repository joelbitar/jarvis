/* Basic Angular structure, the public probably does not need the entire app, When we need to we can always use the gss-app.js file instead */
var app = angular.module('jarvis', [
    'restangular',
    'ngMaterial',

    'ngCookies',
    'ngStorage',

    'ngFocus',

    'jarvis.startpage',
    'jarvis.device',
    'jarvis.devicegroup',
    'jarvis.node',
    'jarvis.sensor',
    'jarvis.admin',
    'jarvis.weather',
    'jarvis.auth',
    'jarvis.signals'
]);

/* Global functions */
var template_url = function(template_name){
    return django.base_ng_template_url + template_name + '?v=' + django.version;
};

// Function needed for when NOT using Restangular, Also used when configuring restangular..
var api_url = function(path){
    if(django.proxy_url != ""){
        return django.proxy_url + 'api/' + path;
    }else{
        return 'api/' + path;
    }
};

app.config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider){
    $httpProvider.interceptors.push(function($q, $location){
        return {
            'response' : function(response){
                return response || $q.when(response);
            },
            'responseError' : function(rejection){
                // If we run in to a Not authorized 401, redirect to login view.
                if(rejection.status === 401 || rejection.status === 403){
                    $location.url('/login/');
                }

                return $q.reject(rejection);
            }
        }
    });
}]);

app.config(['$httpProvider', function($httpProvider){
    // Set the initial CSRF Token from Django view.
    $httpProvider.defaults.headers.common['X-CSRFToken'] = django.csrf_token;

    // Set CSRF Token on all requests that come back from the server.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.config(['$sceDelegateProvider', function($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
            // Allow same origin resource loads.
            'self',
            // Allow loading from our assets domain.  Notice the difference between * and **.
            django.base_static_url + '**'
        ]
    );
}]);

app.directive("include", function ($http, $templateCache, $compile) {
    return {
        restrict: 'A',
        link: function (scope, element, attributes) {
            // The static template URL
            var templateUrl = template_url(attributes.include);

            $http.get(templateUrl, {cache: $templateCache}).success(
                function (tplContent) {
                    element.replaceWith($compile(tplContent)(scope));
                }
            );
        }
    };
});

app.directive("staticSrc", function () {
    return {
        compile: function(elm, attr){
            elm.attr('src', django.base_static_url + elm.attr('static-src'));
            elm.removeAttr('static-src');
        }
    }
});

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('deep-purple')
    .accentPalette('blue');
});

app.config(function(RestangularProvider){
    RestangularProvider.setBaseUrl(api_url(""));
});

app.config(function($mdIconProvider){
    var icons = [
        ['refresh-black', 'ic_autorenew_black_24px'],
        ['refresh-white', 'ic_autorenew_white_24px']
    ];

    _.each(icons, function(image_conf){
        $mdIconProvider.icon(image_conf[0], django.base_static_url + 'images/icons/' + image_conf[1] + '.svg')
    });
});
