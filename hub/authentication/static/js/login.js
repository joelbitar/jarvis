var jarvis_auth = angular.module('jarvis.auth', ['ngRoute', 'restangular']);

jarvis_auth.factory('User', ['$rootScope', 'Restangular',
    function($rootScope, Restangular){
        var User = {
            data : {
                current : false
            },
            loadCurrent : function(){
                console.log('load Current from Server');
                Restangular.one('auth/current').get().then(
                    function(user){
                        // If the user fetched was not a proper one with a pk, it is to be considered false.
                        if(user.pk == undefined){
                            user = false;
                        }

                        User.data.current = user;
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

jarvis_auth.controller('LoginController', ['$scope', '$rootScope', '$http', '$cookies', '$location', 'User', function($scope, $rootScope, $http, $cookies, $location, User) {
    // This object will be filled by the form

    // Set current user to nothing and lazy logout the user if we reach this.
    if(User.data.current != false){
        User.data.current = false;
        $rootScope.$broadcast('loggedOut');
    }

    $scope.login_disabled = false;


    if($cookies.auth_token !== null && $cookies.auth_token !== undefined){
        $http.defaults.headers.common['Authorization'] = 'Token ' + $cookies.auth_token;
        console.log(User);
        User.loadCurrent();
    }

    // Register the login() function
    $scope.login = function(){
        $scope.login_disabled = true;
        $http.post(api_url('auth/login/'), {
                username: $scope.username,
                password: $scope.password
            }
        ).success(function(user){
                // No error: authentication OK
                console.log('success login')
                $scope.login_disabled = false;
                User.data.current = user;
                $rootScope.$broadcast('loggedIn');
                $location.url('/');

                $http.defaults.headers.common['Authorization'] = 'Token ' + user.auth_token;

                // Set cookie.
                $cookies.auth_token = user.auth_token;
            }
        ).error(function(){
                // Error: authentication failed
                delete $http.defaults.headers.common['Authorization'];
                $scope.login_disabled = false;
                $rootScope.loginErrorMessage = "Lösenord och/eller användarnamn stämmde inte :(";
            }
        );
    };
}]);

//authControllers.controller('LogoutController',)
jarvis_auth.controller('LogoutController', ['$scope', '$rootScope', '$location', '$http', 'User', function($scope, $rootScope, $location, $http, User){
    $http.get(api_url('auth/logout/'), {}).success(
        function(response){
            User.data.current = false;
            delete $http.defaults.headers.common['Authorization'];
            $rootScope.$broadcast('loggedOut');
            $location.url('/login');
        }
    )
}]);