/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_device = angular.module('jarvis.device', ['ngRoute', 'restangular'])
.controller('DeviceController', ['$scope', '$rootScope', '$timeout', 'Restangular', function($scope, $rootScope, $timeout, Restangular){
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
                        $rootScope.$broadcast('refresh-groups');
                    }
                );
            }else{
                Restangular.one('devices', device.id).one('command').one('dim').one(device.state + '/').get().then(
                    function(response){
                        console.log(response);
                        $rootScope.$broadcast('refresh-groups');
                    }
                );
            }

            $rootScope.$broadcast('refresh-categories');
        };

        $scope.brightnessSliderChange = function(device){
            wait_for_no_change(device, 500, function(){
                console.log('Change bright ness for real on device', device);
                $scope.sendDeviceState(device);
            });
        };
}]);

jarvis_device.controller('DeviceDetailController', ['$scope', '$routeParams', 'Restangular', function($scope, $routeParams, Restangular){
    console.log($routeParams.id)
    $scope.sendDeviceLearnCommand = function(device){
          Restangular.one('devices', device.id).one('command').one('learn/').get().then(
              function(response){
              }
          );
    };

    Restangular.one('devices', $routeParams.id).one('details/').get().then(
        function(device){
            $scope.device = device;
        }
    )
}]);

jarvis_device.config(['$routeProvider', function($routeProvider){
    $routeProvider.when(
        '/device/:id/', {
            templateUrl: template_url('device-detail.html'),
            controller: 'DeviceDetailController'
        }
    )
}]);
