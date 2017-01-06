var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', '$rootScope', '$window', 'Restangular', 'focus',  function($scope, $rootScope, $window, Restangular, focus) {
        focus.broadcast('refresh-devices');

        // Update device without setting everything again.
        $scope.updateDevice = function(device){
            $scope.devices.forEach(function(d){
                if(d.id == device.id){
                    d.state = device.state;
                }
            });
        };

        get_categories_from_devices = function(category_name){
            var a = [];

            // Loop through each of the categories
            _.each(_.uniq(_.filter(_.map($scope.devices, category_name)), function(o){return o.id}), function (item_original) {
                var category_devices, state = 0, item = angular.copy(item_original);

                // Get devices for this category
                category_devices = _.filter(
                    $scope.devices,
                    function(o){
                        if(_.has(o[category_name], 'id')){
                            return o[category_name]['id'] == item.id;
                        }
                    }
                );

                // Check if there is any device that is NOT turned off.
                _.each(category_devices, function(device){
                    if(device.state != 0){
                        state = 1;
                        return false;
                    }
                });

                item['state'] = state;
                item['devices'] = category_devices;

                a.push(
                   item
                )
            });

            return a;
        };

        $scope.$on('refresh-categories', function(){
            $scope.placements = get_categories_from_devices('placement');
            $scope.rooms = get_categories_from_devices('room');

            console.log('placements', $scope.placements);
            console.log('rooms', $scope.rooms);
        });

        $scope.$on('refresh-devices', function(){
            Restangular.all('devices/').getList().then(function(devices){
                if($scope.devices !== undefined){
                    devices.forEach($scope.updateDevice);
                }else{
                    $scope.devices = devices;
                }

                $scope.$broadcast('refresh-categories');
            });
        });

        $scope.$broadcast('refresh-devices');
}]).controller('StartpagePlacementController', ['$scope', '$rootScope','Restangular', function($scope, $rootScope,Restangular) {
        var set_devices_state = function(placement){
            _.each(
                placement.devices,
                function(device){
                    device.state = (function(placement_state){
                        // If dimmable set to 255 or 0
                        if(device.is_dimmable){
                            return placement_state ? 255 : 0;
                        }

                        return placement_state;
                    }(placement.state))
                }
            );
        };
        $scope.togglePlacement = function(placement){
            placement.state = placement.state ? 0 : 1;

            set_devices_state(placement);

            $scope.sendPlacementState(placement);
        };



        $scope.sendPlacementState = function(placement){
            console.info('Send room state');
            set_devices_state(placement);

            Restangular.one('placements', placement.id).one('command').one(String(placement.state ? 'on' : 'off') + '/').get().then(
                function(response){
                    console.log('placement command', response);
                    $rootScope.$broadcast('refresh-groups');
                }
            );
        };

}]).controller('StartpageRoomController', ['$scope', '$rootScope', 'Restangular', function($scope, $rootScope, Restangular) {
        var set_devices_state = function(room){
            _.each(
                room.devices,
                function(device){
                    device.state = (function(room_state){
                        // If dimmable set to 255 or 0
                        if(device.is_dimmable){
                            return room_state ? 255 : 0;
                        }

                        return room_state;
                    }(room.state))
                }
            );
        };

        $scope.toggleRoom = function(room){
            room.state = room.state ? 0 : 1;

            set_devices_state(room);

            $scope.sendRoomState(room);
        };

        $scope.sendRoomState = function(room){
            console.info('Send room state');

            set_devices_state(room);

            Restangular.one('rooms', room.id).one('command').one(String(room.state ? 'on' : 'off') + '/').get().then(
                function(response){
                    console.log('room command', response);
                    $rootScope.$broadcast('refresh-groups');
                }
            );
        };

}]).controller('StartpageForecastController', ['$scope', '$window', 'focus',  'Restangular', function($scope, $window, focus, Restangular) {
        focus.broadcast('refresh-forecast');

        $scope.$on('refresh-forecast', function(){
            Restangular.all('forecast/short/').getList().then(function(forecasts){
                $scope.forecasts = [];

                forecasts.forEach(function(forecast_group){
                    $scope.forecasts = $scope.forecasts.concat(forecast_group);
                });
            });
        });

        $scope.$broadcast('refresh-forceast');

}])
.controller('StartpageSensorController', ['$scope', 'focus', 'Restangular',  function($scope, focus, Restangular) {
        focus.broadcast('refresh-sensors');

        $scope.$on('refresh-sensors', function(){
            Restangular.all('sensors/').getList().then(function(sensors){
                $scope.sensors = sensors;
            });
        });

        $scope.$broadcast('refresh-sensors');

}]).controller('StartpageDeviceGroupController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        $scope.$on('refresh-groups', function() {
            Restangular.all('groups/').getList().then(function (groups) {
                $scope.groups = groups;
            });
        });
        // Load groups on first run (aka refresh)
        $scope.$broadcast('refresh-groups');
}]).controller('ToolbarController', ['$scope', '$rootScope', function($scope, $rootScope){
        $scope.refresh = function(){
            _.each(
                [
                    'refresh-devices',
                    'refresh-forecast',
                    'refresh-sensors',
                    'refresh-groups'
                ],
                function(signal_name){
                    $rootScope.$broadcast(signal_name);
                }
            );
        };
}]);


