/**
 *
 * Created by joel on 2015-03-06.
 */

var jarvis_node = angular.module('jarvis.node', ['ngRoute', 'restangular'])
.controller('NodeController', ['$scope', '$rootScope', 'Restangular', function($scope, $rootScope, Restangular){
        Restangular.all('nodes').getList().then(function (nodes) {
            $scope.nodes = nodes;
        });
}]);

jarvis_node.controller('NodeDetailController', ['$scope', '$routeParams', 'Restangular', function($scope, $routeParams, Restangular){
    $scope.sendNodeCommand = function(command_name){
        Restangular.one('nodes', $scope.node.id).one(command_name + '/').get().then(
            function(response){
                console.log('Response', response);
            }
        )
    };

    Restangular.one('nodes', $routeParams.id).one('details/').get().then(
        function(node){
            console.log('hej');

            $scope.node = node;
        }
    )
}]);

jarvis_device.config(['$routeProvider', function($routeProvider){
    $routeProvider.when(
        '/nodes/', {
            templateUrl: template_url('nodes.html'),
            controller: 'NodeController'
        }
    )
}]);

jarvis_device.config(['$routeProvider', function($routeProvider){
    $routeProvider.when(
        '/nodes/:id/', {
            templateUrl: template_url('node-detail.html'),
            controller: 'NodeDetailController'
        }
    )
}]);
