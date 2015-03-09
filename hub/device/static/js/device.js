/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_device = angular.module('jarvis.device', ['ngRoute', 'restangular'])
.controller('DeviceController', ['$scope', '$timeout', 'Restangular', function($scope, $timeout, Restangular){
        var last_change = {};

        var wait_for_no_change_timeout = function(device, timeout, callback){
            var current_time = new Date().getTime();
            var lc = last_change[device.id];
            lc.iteration += 1;


            if(lc.iteration > 1 && current_time - lc.timestamp > timeout){
                // Delete in last_change
                delete last_change[device.id];

                // Call callback
                callback();

                return undefined;
            }

            $timeout(
                function(){
                    wait_for_no_change_timeout(device, timeout, callback)
                },
                50
            )
        };

        var wait_for_no_change = function(device, timeout, callback){

            var current_time = new Date().getTime();

            var lc = last_change[device.id];

            last_change[device.id] = {
                'timestamp' : parseInt(current_time),
                'device' : device,
                'iteration' : 0
            };

            if(lc === undefined){
                last_change[device.id]['first_timestamp'] = current_time;
                wait_for_no_change_timeout(device, timeout, callback);
            }

        };

        $scope.toggleDevice = function(device){
            if(device.is_dimmable == false){
                // Switch states
                device.state = device.state ? 0 : 1;

            }else{
                if(device.state > 80){
                    device.state = 0;
                }else{
                    device.state = 255;
                }
            }

            $scope.sendDeviceState(device);
        };

        $scope.sendDeviceState = function(device){
            console.info('Send device state');

            if(device.is_dimmable === false){
                console.log(device.state);

                var command_verb = device.state ? 'on' : 'off';

                Restangular.one('devices', device.id).one('command').one(command_verb + '/').get().then(
                    function(response){
                        console.log(response);
                    }
                );
            }else{

            }
        };

        $scope.brightnessSliderChange = function(device){
            wait_for_no_change(device, 500, function(){
                console.log('Change bright ness for real on device', device);
                $scope.sendDeviceState(device);
            });
        };


}]);
