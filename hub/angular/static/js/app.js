/* Basic Angular structure, the public probably does not need the entire app, When we need to we can always use the gss-app.js file instead */
var app = angular.module('jarvis', [
    'restangular',
    'ngMaterial',

    'jarvis.startpage',
    'jarvis.device'
]);

app.directive("include", function ($http, $templateCache, $compile) {
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
    .primaryPalette('pink')
    .accentPalette('blue');
});

app.config(function(RestangularProvider){
    if(django.proxy_url != ""){
        RestangularProvider.setBaseUrl('/' + django.proxy_url);
    }else{
        RestangularProvider.setBaseUrl('/api/');
    }
});

/* Global functions */
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


