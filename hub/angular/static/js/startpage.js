
var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        $scope.$on('refresh-devices', function(){
            Restangular.all('devices').getList().then(function(devices){
                $scope.devices = devices;
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


