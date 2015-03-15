var jarvis_sensor = angular.module('jarvis.sensor', ['ngRoute', 'restangular'])
    .controller('SensorController', ['$scope', 'Restangular', function($scope, Restangular){

    }]
).controller('SensorDetailController', ['$scope', '$routeParams', 'Restangular', function($scope, $routeParams, Restangular){
        Restangular.one('sensors', $routeParams.id).get().then(
            function(sensor){
                $scope.sensor = sensor;
            }
        );

        Restangular.one('sensors', $routeParams.id).one('logs/').getList().then(
            function(logs){
                $scope.sensor_logs = logs;
            }
        )
    }]
);

jarvis_sensor.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/sensors/:id/',
            {
                templateUrl : template_url('sensor-detail.html'),
                controller: 'SensorDetailController'
            }
        )
    }]
);
