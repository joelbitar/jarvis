/**
 *
 * Created by joel on 2015-03-25.
*/

var jarvis_weather = angular.module('jarvis.weather', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/weather/', {
                templateUrl: template_url('weather.html')
            }
        )
}]).controller('WeatherController', ['$scope', 'Restangular', function($scope, Restangular){
    Restangular.all('forecast/detailed/').getList().then(function(forecasts){
        console.log(forecasts);
        $scope.forecast_groups = forecasts;
    });
}]);

