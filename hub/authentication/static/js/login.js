var jarvis_auth = angular.module('jarvis.auth', ['ngRoute', 'restangular']);

jarvis_auth.run(['$rootScope', '$cookies', '$http', 'User', function($rootScope, $cookies, $http, User){
    // Sets Auth token if found in cookies and loads user with Username and that.
    if(User.getAuthCookie() !== undefined){
        User.setAuthHeaders();
        User.loadCurrent();
    }
}]);

jarvis_auth.factory('User', ['$rootScope', '$cookies', '$http', 'Restangular',
    function($rootScope, $cookies, $http, Restangular){
        var User = {
            data : {
                current : false
            },
            loadCurrent : function(){
                Restangular.one('auth/current').get().then(
                    function(user){
                        // If the user fetched was not a proper one with a pk, it is to be considered false.
                        // Otherwise, set it to the user we got.
                        User.data.current = (function(u){
                            if(!u.pk){
                                return false;
                            }
                            return u;
                        }(user));

                        $rootScope.$broadcast('loggedIn');
                    }
                )
            },
            setAuthCookie : function (auth_token){
                $cookies.auth_token = auth_token;
                return this;
            },
            getAuthCookie : function (){
                if($cookies.auth_token !== null && $cookies.auth_token !== undefined){
                    return $cookies.auth_token;
                }

                return undefined;
            },
            /*
            * Set Authentication token, defaults to using token found in cookies.
            */
            setAuthHeaders : function (auth_token){
                if(auth_token === undefined){
                    auth_token = $cookies.auth_token;
                }

                $http.defaults.headers.common['Authorization'] = 'Token ' + auth_token;
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


    $rootScope.$on('loggedIn', function(){
        console.log('user has logged in!')
    });

    // Register the login() function
    $scope.login = function(){
        $scope.login_disabled = true;
        $http.post(api_url('auth/login/'), {
                username: $scope.username,
                password: $scope.password
            }
        ).success(function(user){
                // No error: authentication OK
                $scope.login_disabled = false;
                User.data.current = user;
                $rootScope.$broadcast('loggedIn');
                $location.url('/');

                // Sets auth Cookie then set auth headers
                User.setAuthCookie(user.auth_token).setAuthHeaders();
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
            console.log('send user to login');
            $location.url('/login');
        }
    )
}]);