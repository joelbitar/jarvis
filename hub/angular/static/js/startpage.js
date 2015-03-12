
var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all('devices').getList().then(function(devices){
            $scope.devices = devices;
        });
}])
.controller('StartpageSensorController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all('sensors').getList().then(function(sensors){
            $scope.sensors = sensors;
        });
}]).controller('StartpageDeviceGroupController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all('groups').getList().then(function(sensors){
            $scope.groups = groups;
        });
}]);


