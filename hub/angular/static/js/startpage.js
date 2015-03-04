/**
 *
 * Created by joel on 2015-03-02.
 */

var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute', 'restangular'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                'templateUrl' : template_url('startpage.html')
            }
        );
}])
.controller('StartpageDeviceController', ['$scope', 'Restangular',  function($scope, Restangular) {
        Restangular.all(api_url('devices')).getList().then(function(devices){
            $scope.devices = devices;
            console.log(devices);
        });

        $scope.toggleDevice = function(device){
            console.log('test', device);
            device.state = !device.state;
        }
}]);
