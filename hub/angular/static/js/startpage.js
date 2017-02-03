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
            //_.set(_.find(_.flatten(_.map(_.flatten(_.values($scope.device_categories)), 'devices')), {id: device.id}), 'state', device.state)
            var old_device = _.find(
                _.flatten(
                    _.map(
                        _.flatten(
                            _.values($scope.device_categories)
                        ),
                        'devices'
                    )
                ),
                {
                    id: device.id
                }
            );

            if(_.isUndefined(old_device)){
                console.warn('Could not find device ', device.id);
                return undefined;
            }

            // device change is newer or the same as the one we are trying to update with.
            if(moment(old_device.changed).diff(device.changed) >= 0){
                return undefined;
            }

            // Set device properties.
            _.each(['changed', 'state'], function(property_name){
                _.set(old_device, property_name, _.get(device, property_name));
            });
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
        };

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

                                    if(typeof(category_relation) === 'object'){
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

                        $scope.device_categories[category_name] = category_items;
                    });
                }
            );

        };

        $scope.$on('refresh-devices', function() {
            // If there is no devices, get all the names and whatnot
            if (_.size($scope.device_categories) == 0) {
                Restangular.all('devices/short/').getList().then(function (devices) {
                    add_devices_to_categories(devices);
                });
            }else{
                // If there is devices, just get the states
                Restangular.all('devices/states/').getList().then(function (devices) {
                    devices.forEach($scope.updateDevice);
                });
            }
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
        $scope.grouped_forecasts = {};

        focus.broadcast('refresh-forecast');

        $scope.$on('refresh-forecast', function(){
            Restangular.all('forecast/short/').getList().then(function(forecasts){
                var grouped_forcecasts, existing_days, new_days;

                grouped_forcecasts = _.groupBy(
                    _.flatten(forecasts),
                    function(forecast){
                        // Valid time or valid_time_min, whatevva
                        var valid_time = _.get(forecast, 'valid_time', _.get(forecast, 'valid_time__min'));

                        // Just the date-part.
                        return String(valid_time).slice(0, 10)
                    }
                );

                new_days = _.keys(grouped_forcecasts);

                // Remove old days
                _.each(_.difference(_.keys($scope.grouped_forecasts), new_days), function (day_to_remove) {
                    _.pullAt(
                        $scope.grouped_forecasts,
                        _.indexOf(_.keys($scope.grouped_forecasts), day_to_remove)
                    );
                });

                // Go over all groups
                _.each(grouped_forcecasts, function(forecasts, new_day){
                    _.each(forecasts, function(forecast){
                        // Now we are at the new forecast,
                        var old_forecast = _.find(
                            _.get(
                                $scope.grouped_forecasts, new_day
                            ),
                            function(old_forecast){
                                var old_valid_time, new_valid_time;

                                old_valid_time = _.get(old_forecast, 'valid_time', _.get(old_forecast, 'valid_time__min'));
                                new_valid_time = _.get(forecast, 'valid_time', _.get(forecast, 'valid_time__min'));

                                return old_valid_time == new_valid_time;
                            }
                        );

                        if(_.has(old_forecast, 'valid_time__min')){
                            // Old forecast had valid_time__min
                            delete old_forecast['valid_time__min'];
                        }

                        if(_.has(old_forecast, 'valid_time__max')){
                            // Old forecast had valid_time__min
                            delete old_forecast['valid_time__max'];
                        }

                        if(_.has(old_forecast, 'valid_time')){
                            // Old forecast had valid_time__min
                            delete old_forecast['valid_time'];
                        }

                        // Set new properties.
                        _.each(_.keys(forecast), function(property_name){
                            _.set(old_forecast, property_name, _.get(forecast, property_name));
                        })
                    });
                });

                // Add new days
                _.each(_.difference(new_days, _.keys($scope.grouped_forecasts)), function (day_to_add) {
                    if(!day_to_add || day_to_add === "null"){
                        return true;
                    }

                    // Set new a new grouped forecast
                    _.set(
                        $scope.grouped_forecasts,
                        // Day key
                        day_to_add,
                        // All items in the new forecasts
                        _.get(
                            grouped_forcecasts,
                            day_to_add
                        )
                    );
                });
            });
        });

        $scope.$broadcast('refresh-forecast');
}])
.controller('StartpageSensorController', ['$scope', 'focus', 'Restangular',  function($scope, focus, Restangular) {
        $scope.sensors = undefined;
        focus.broadcast('refresh-sensors');

        $scope.refreshSensorHistory = function(){
            Restangular.all('sensors/history/').getList({
                hours: 24
            }).then(
                function(response){
                    _.each(
                        _.groupBy(response.plain(), 'sensor'),
                        function(raw_history, sensor_id){
                            var history_data, sensor, last_history_item = _.last(raw_history);
                            sensor = _.find($scope.sensors, {id: parseInt(sensor_id)});
                            if(_.isUndefined(sensor)){
                                // continue to next sensor
                                return undefined;
                            }

                            history_data =_.map(
                                raw_history,
                                function(history_item){
                                    return parseFloat(
                                        _.get(history_item, 'temperature_avg')
                                    )
                                }
                            );

                            sensor.history = {
                                categories: _.map(raw_history, function(history_item){
                                    return moment(history_item.date_time).format('HH')
                                }),
                                series: [
                                    {
                                        data: history_data
                                    }
                                ]
                            };

                            sensor.updated = _.get(last_history_item, 'updated');
                            sensor.temperature = _.get(last_history_item, 'temperature_latest');
                            sensor.humidity = _.get(last_history_item, 'humidity_latest');
                        }
                    );
                }
            )


        };

        $scope.$on('refresh-sensors', function(){
            if(_.isUndefined($scope.sensors)){
                Restangular.all('sensors/').getList().then(function(response){
                    $scope.sensors = response.plain();
                    $scope.refreshSensorHistory();
                });
            }else{
                $scope.refreshSensorHistory();
            }
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


