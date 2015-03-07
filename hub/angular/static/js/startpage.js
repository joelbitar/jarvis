
var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all(api_url('devices')).getList().then(function(devices){
            $scope.devices = devices;
        });
}])
.controller('StartpageSensorController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all(api_url('sensors')).getList().then(function(sensors){
            $scope.sensors = sensors;
            console.log(sensors)
        });
}]);


