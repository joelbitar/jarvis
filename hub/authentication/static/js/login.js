var jarvis_auth = angular.module('jarvis.auth', ['ngRoute', 'restangular']);

jarvis_auth.factory('User', ['$rootScope', 'Restangular',
    function($rootScope, Restangular){
        var User = {
            data : {
                current : false
            },
            loadCurrent : function(){
                console.log('load Current from Server');
                Restangular.one('/api/auth/currentuser').one().then(
                    function(user){
                        // If the user fetched was not a proper one with a pk, it is to be considered false.
                        if(data.pk == undefined){
                            data = false;
                        }

                        User.data.current = data;
                        $rootScope.$broadcast('loggedIn');
                    }
                )
            }
        };

        return User;
    }
]);

jarvis_auth.config(['$routeProvider', function($routeProvider){
    $routeProvider.when(
        '/login/', {
            templateUrl : template_url('login.html')
        }
    )
}]);

jarvis_auth.controller('LoginController', ['$scope', '$rootScope', '$http', '$location', 'User', function($scope, $rootScope, $http, $location, User) {
    // This object will be filled by the form

    // Set current user to nothing and lazy logout the user if we reach this.
    if(User.data.current != false){
        User.data.current = false;
        $rootScope.$broadcast('loggedOut');
    }

    $scope.login_disabled = false;

    // Register the login() function
    $scope.login = function(){
        $scope.login_disabled = true;
        $http.post('/api/auth/login/', {
            username: $scope.username,
            password: $scope.password
        }
    ).success(function(user){
        // No error: authentication OK

        $scope.login_disabled = false;
        User.data.current = user;
        $rootScope.$broadcast('loggedIn');
        $location.url('/');
    }).error(function(){
         // Error: authentication failed
        $scope.login_disabled = false;
        $rootScope.loginErrorMessage = "Lösenord och/eller användarnamn stämmde inte :(";
    });
  };
}]);

//authControllers.controller('LogoutController',)
jarvis_auth.controller('LogoutController', ['$scope', '$rootScope', '$location', '$http', 'User', function($scope, $rootScope, $location, $http, User){
    $http.get('/api/auth/logout/', {}).success(
        function(response){
            User.data.current = false;
            $rootScope.$broadcast('loggedOut');
            $location.url('/login');
        }
    )
}]);