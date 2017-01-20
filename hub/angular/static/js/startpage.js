var jarvis_startpage = angular.module('jarvis.startpage', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/', {
                templateUrl: template_url('startpage.html')
            }
        )
}])
.controller('StartpageDeviceController', ['$scope', '$q', '$rootScope', '$window', 'Restangular', 'focus',  function($scope, $q, $rootScope, $window, Restangular, focus) {
        var fetch_categories_promises = {};

        fetch_categories_promises['room'] = undefined;
        fetch_categories_promises['placement'] = undefined;

        $scope.device_categories = {};

        // Update device without setting everything again.
        $scope.updateDevice = function(device){
            console.error('Need a way to update devices');
            return;
            /*
            devices.forEach(function(d){
                if(d.id == device.id){
                    d.state = device.state;
                }
            });
            */
        };

        get_category_object = function(json){
            var o = angular.copy(json);

            o.get_state = function(){
                return _.size(
                    _.filter(
                        this.devices,
                        function(device){
                            return device.state != 0;
                        }
                    )
                ) > 0;
            };

            return o;
        }

        add_devices_to_categories = function (devices) {
            var fetch_category_deferred, categories, requests = [];

            categories = [
                'room',
                'placement',
                'group'
            ];

            _.each(categories, function(category_name){
                requests.push(Restangular.all(category_name + 's/').getList().then());
            });

            $q.all(requests).then(
                function(responses){
                    _.each(responses, function (response, i) {
                        var category_items = [],  category_name = categories[i];
                        // category_items       Array of items in this category     [room, room, room]
                        // category_name        String name of the category type    "room", "group", "placement"

                        _.each(response, function(category_response){
                            var category_object = get_category_object(category_response.plain());
                            // category_object      Wrapper around the response json with extra functions and properties on the category object

                            category_object.devices = _.filter(
                                devices,
                                // Filter to only include devices that are on this specific room type
                                function(device){
                                    var category_relation;

                                    category_relation = _.get(device, category_name, _.get(device, category_name + 's'));
                                    // Category relation can be both an array of ids or a single id
                                    // category_relation = 1, or [1,2,3]

                                    if(category_name == "group"){
                                        console.info(category_object.name);
                                        console.log(category_object);
                                        console.log(category_relation)
                                    }

                                    if(typeof(category_relation) === 'object'){
                                        console.log(device.groups);
                                        // Is a list if category_object.id is amongst the category relations, add it.
                                        return _.indexOf(category_relation, category_object.id) >= 0;
                                    }

                                    return category_relation == category_object.id;
                                }
                            );

                            // Add category object to items
                            category_items.push(
                                category_object
                            );
                        });

                        console.log(category_name, category_items);
                        $scope.device_categories[category_name] = category_items;
                    });

                    console.log($scope.device_categories);
                }
            );

        };

        $scope.$on('refresh-devices', function() {
            Restangular.all('devices/short/').getList().then(function (devices) {
                if (_.size($scope.device_categories) > 0) {
                    devices.forEach($scope.updateDevice);
                } else {
                    add_devices_to_categories(devices);
                }
            })
        });

        $scope.$broadcast('refresh-devices');
        focus.broadcast('refresh-devices');

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
            set_devices_state(placement);

            Restangular.one('placements', placement.id).one('command').one(String(placement.state ? 'on' : 'off') + '/').get().then(
                function(response){
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

            set_devices_state(room);

            Restangular.one('rooms', room.id).one('command').one(String(room.state ? 'on' : 'off') + '/').get().then(
                function(response){
                    $rootScope.$broadcast('refresh-groups');
                }
            );
        };

}]).controller('StartpageForecastController', ['$scope', '$window', 'focus',  'Restangular', function($scope, $window, focus, Restangular) {
        focus.broadcast('refresh-forecast');

        $scope.$on('refresh-forecast', function(){
            delete $scope.grouped_forecasts;

            Restangular.all('forecast/short/').getList().then(function(forecasts){
                $scope.grouped_forecasts = _.groupBy(
                    _.flatten(forecasts),
                    function(forecast){
                        // Valid time or valid_time_min, whatevva
                        var valid_time = _.get(forecast, 'valid_time', _.get(forecast, 'valid_time__min'));

                        // Just the date-part.
                        return String(valid_time).slice(0, 10)
                    }
                );

                console.log($scope.grouped_forecasts);
            });
        });

        $scope.$broadcast('refresh-forecast');
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


