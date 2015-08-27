var jarvis_admin = angular.module('jarvis.admin', ['ngRoute'])
.config(['$routeProvider', function($routeProvider){
        $routeProvider.when(
            '/administration/', {
                templateUrl: template_url('admin/index.html')
            }
        ).when(
                '/administration/recent-signals/', {
                templateUrl: template_url('admin/recent-signals.html')
            }
        )
}])
.controller('SettingsController', ['$scope', '$rootScope', 'Restangular',  function($scope, $rootScope, Restangular) {
        console.log('apa');
}]);