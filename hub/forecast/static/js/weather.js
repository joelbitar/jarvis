/**
 *
 * Created by joel on 2015-03-25.
 */

var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/weather/', {
                templateUrl: template_url('weather.html')
            }
        )
}])
.controller('WeatherController', ['$scope', 'Restangular', function($scope, Restangular){
    Restangular.all('forecasts').getList().then(function(forecasts){
        console.log(forecasts);
        $scope.forecasts = forecasts;
    });
}]);
