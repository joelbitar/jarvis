/* Basic Angular structure, the public probably does not need the entire app, When we need to we can always use the gss-app.js file instead */
var gss = angular.module('jarvis',
    [
        'restangular',
        'ui.bootstrap',

        'jarvis.startpage'
    ]
);

gss.config(['$sceDelegateProvider', function($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
        // Allow same origin resource loads.
        'self',
        // Allow loading from our assets domain.  Notice the difference between * and **.
        //'http://*.teebovirtualbox.lc/**',
        //'http://*.teebo.se/**'
        django.static_url + '**'
    ]
    );
}]);

gss.config(['$httpProvider', function($httpProvider){
    // Set the initial CSRF Token from Django view.
    $httpProvider.defaults.headers.common['X-CSRFToken'] = django.csrf_token;

    // Set CSRF Token on all requests that come back from the server.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

gss.directive("include", function ($http, $templateCache, $compile) {
    return {
        restrict: 'A',
        link: function (scope, element, attributes) {
            // The static template URL
            var templateUrl = django.base_ng_template_url + attributes.include;

            $http.get(templateUrl, {cache: $templateCache}).success(
                function (tplContent) {
                    element.replaceWith($compile(tplContent)(scope));
                }
            );
        }
    };
});

gss.directive("staticSrc", function () {
    return {
        compile: function(elm, attr){
            elm.attr('src', django.base_static_url + elm.attr('static-src'));
            elm.removeAttr('static-src');
        }
    }
});

gss.directive('myCustomer', function() {
  return {
    template: 'Name: {{customer.name}} Address: {{customer.address}}'
  };
});

var template_url = function(template_name){
    return django.base_ng_template_url + template_name
};

var api_url = function(path){
    if(django.proxy_url == ""){
        return django.proxy_url + path;
    }else{
        return 'api/' + path;
    }
};
