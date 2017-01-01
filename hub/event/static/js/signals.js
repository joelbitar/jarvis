var jarvis_signals = angular.module('jarvis.signals', ['ngRoute'])
    .controller('RecentSignalsController', ['$scope', 'Restangular', function($scope, Restangular){
        Restangular.all('signals/recent/').getList().then(function(result){
            $scope.signals = result;
        });
}]);
