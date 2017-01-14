/**
 *
 * Created by joel on 2015-03-25.
*/

var jarvis_weather = angular.module('jarvis.weather', ['ngRoute'])
    .factory('WeatherIcon', [function(){
        return {
            'wind' : function(forecast){
                var closest, choices = [
                    0,
                    23,
                    45,
                    68,
                    90,
                    113,
                    135,
                    158,
                    180,
                    203,
                    225,
                    248,
                    270,
                    293,
                    313,
                    336
                ];

                closest = choices.reduce(function (prev, curr) {
                    return (Math.abs(curr - forecast.wd) < Math.abs(prev - forecast.wd) ? curr : prev);
                });

                return 'towards-' + String(closest) + '-deg';

            },
            'weather' : function (forecast){
                var valid_time, icon_parts = [], night_time = false;

                if(forecast.valid_time !== undefined){
                    valid_time = new Date(forecast.valid_time);
                }else{
                    valid_time = new Date(forecast.valid_time__min)
                }

                if(valid_time.getHours() > 20 || valid_time.getHours() < 7){
                    night_time = true;
                }

                if(night_time){
                    // At night
                    icon_parts.push('night-alt')
                }else{
                    // If it is not that much clouds
                    if(forecast.tcc <= 6){
                        icon_parts.push('day')
                    }
                }

                // If any rain
                if(forecast.pcat !== 0){
                    // Percipitation category
                    icon_parts.push(function(){
                        if(forecast.tstm > 50){
                            // If more than 50% chance of thunder.
                            return 'storm-showers'
                        }

                        switch (forecast.pcat){
                            case 1:
                                // Snow
                                return 'snow';
                            case 2:
                                // Snow and rain
                                return 'rain-mix';
                            case 3:
                                // Rain
                                if(forecast.ws >= 5){
                                    return 'rain-wind';
                                }
                                return 'rain';
                            case 4:
                                // Drizzle
                                return 'showers';
                            case 5:
                                // Freezing rain
                                return 'hail';
                            case 6:
                                // Freezing drizzle
                                return 'hail';
                        }
                    }())
                }else{
                    // No rain, lets see if we have special cases
                    if(forecast.tstm > 50){
                        // Thunder
                        icon_parts.push('lightning');
                    }else if(forecast.tcc >= 4){
                        // Cloudy
                        icon_parts.push('cloudy');
                    }else{
                        // Special cases.
                        if(night_time){
                            if(forecast.tcc >= 2){
                                // the partly cloudy does not conform with the other ones at all.
                                icon_parts = ['night-partly-cloudy']
                            }else{
                                icon_parts = ['night-clear'];
                            }
                        }else{
                            if(forecast.tcc >= 2){
                                icon_parts.push('sunny-overcast')
                            }else{
                                icon_parts.push('sunny');
                            }
                        }
                    }
                }

                icon_parts.unshift('wi');

                return icon_parts.join('-')
            }
        }
    }])
    .controller('WeatherIconController', ['$scope', 'WeatherIcon', function($scope, WeatherIcon){
        $scope.weather_icon_class = WeatherIcon.weather($scope.forecast);
    }])
    .directive('weatherIcon', function(){
        return {
            templateUrl : template_url('directive/weather-icon.html'),
            restrict: 'E',
            scope : {
                forecast : '='
            }
        }
    })
    .controller('WindIconController', ['$scope', 'WeatherIcon', function($scope, WeatherIcon){
        $scope.weather_icon_class = WeatherIcon.wind($scope.forecast);
    }])
    .directive('windIcon', function(){
        return {
            templateUrl : template_url('directive/wind-icon.html'),
            restrict: 'E',
            scope : {
                forecast : '='
            }
        }
    })
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

