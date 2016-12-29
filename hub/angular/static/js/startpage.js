var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', '$rootScope', '$window', 'Restangular', 'focus',  function($scope, $rootScope, $window, Restangular, focus) {
        focus.broadcast('refresh-devices');

        // Update device without setting everything again.
        $scope.updateDevice = function(device){
            $scope.devices.forEach(function(d){
                if(d.id == device.id){
                    d.state = device.state;
                }
            });
        };

        $scope.$on('refresh-devices', function(){
            Restangular.all('devices/').getList().then(function(devices){
                if($scope.devices !== undefined){
                    devices.forEach($scope.updateDevice);
                }else{
                    $scope.devices = devices;
                }
            });
        });

        $scope.$broadcast('refresh-devices');

}]).controller('StartpageForecastController', ['$scope', '$window', 'focus',  'Restangular', function($scope, $window, focus, Restangular) {
        focus.broadcast('refresh-forecast');

        $scope.$on('refresh-forecast', function(){
            Restangular.all('forecast/short/').getList().then(function(forecasts){
                $scope.forecasts = [];

                forecasts.forEach(function(forecast_group){
                    $scope.forecasts = $scope.forecasts.concat(forecast_group);
                });
            });
        });

        $scope.$broadcast('refresh-forceast');

}])
.controller('StartpageSensorController', ['$scope', 'focus', 'Restangular',  function($scope, focus, Restangular) {
        focus.broadcast('refresh-sensors');

        $scope.$on('refresh-sensors', function(){
            Restangular.all('sensors/').getList().then(function(sensors){
                $scope.sensors = sensors;
            });
        });

        $scope.$broadcast('refresh-sensors');

}]).controller('StartpageDeviceGroupController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        $scope.$on('refresh-groups', function() {
            Restangular.all('groups/').getList().then(function (groups) {
                $scope.groups = groups;
            });
        });
        // Load groups on first run (aka refresh)
        $scope.$broadcast('refresh-groups');
}]).controller('ToolbarController', ['$scope', '$rootScope', function($scope, $rootScope){
        $scope.refresh = function(){
            _.each(
                [
                    'refresh-devices',
                    'refresh-forecast',
                    'refresh-sensors',
                    'refresh-groups'
                ],
                function(signal_name){
                    $rootScope.$broadcast(signal_name);
                }
            );
        };
}]);


