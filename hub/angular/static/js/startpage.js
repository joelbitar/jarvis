
var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        // Update device without setting everything again.
        $scope.updateDevice = function(device){
            $scope.devices.forEach(function(d){
                if(d.id == device.id){
                    d.state = device.state;
                }
            });
        };

        $scope.$on('refresh-devices', function(){
            Restangular.all('devices').getList().then(function(devices){
                if($scope.devices !== undefined){
                    devices.forEach($scope.updateDevice);
                }else{
                    $scope.devices = devices;
                }
            });
        });
        $scope.$broadcast('refresh-devices');
}])
.controller('StartpageSensorController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all('sensors').getList().then(function(sensors){
            $scope.sensors = sensors;
        });
}]).controller('StartpageDeviceGroupController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        $scope.$on('refresh-groups', function() {
            Restangular.all('groups').getList().then(function (groups) {
                $scope.groups = groups;
            });
        });
        $scope.$broadcast('refresh-groups');
}]);


