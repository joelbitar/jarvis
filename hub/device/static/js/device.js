/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_device = angular.module('jarvis.device', ['ngRoute', 'restangular'])
.controller('DeviceController', ['$scope', 'Restangular', function($scope, Restangular){
        $scope.toggleDevice = function(device){
            console.log('toggleDevice in device.js');
            device.state = !device.state;
        };
}]);
