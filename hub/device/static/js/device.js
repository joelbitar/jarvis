/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_device = angular.module('jarvis.device', ['ngRoute', 'restangular'])
.controller('DeviceController', ['$scope', 'Restangular', function($scope, Restangular){

        $scope.toggleDevice = function(device){
            if(device.is_dimmable == false){
                device.state = !device.state;
            }else{
                if(device.state > 80){
                    device.state = 0;
                }else{
                    device.state = 100;
                }
            }
        };

}]);
