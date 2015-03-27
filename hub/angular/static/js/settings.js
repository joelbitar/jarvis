var jarvis_settinsg = angular.module('jarvis.settings', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/settings/', {
                templateUrl: template_url('settings.html')
            }
        )
}])
.controller('SettingsController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        console.log('apa');
}]);