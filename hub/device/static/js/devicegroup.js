/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_devicegroup = angular.module('jarvis.devicegroup', ['ngRoute', 'restangular'])
.controller('DeviceGroupController', ['$scope', '$rootScope', 'Restangular', function($scope, $rootScope, Restangular){
        var last_change = {};

        $scope.toggleDeviceGroup = function(group){
            group.state = !group.state;
            $scope.sendDeviceGroupState(group);
        };

        $scope.sendDeviceGroupState = function(device){
            console.info('Send device-group state');

            var command_verb = device.state ? 'on' : 'off';

            Restangular.one('devicegroups', device.id).one('command').one(command_verb + '/').get().then(
                function(response){
                    console.log('Refresh devices...');
                    $rootScope.$broadcast('refresh-devices');
                }
            );
        };
}]);
