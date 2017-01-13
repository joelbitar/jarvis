var jarvis_auth = angular.module('jarvis.auth', ['ngRoute', 'restangular']);

jarvis_auth.run(['$rootScope', '$cookies', '$http', 'User', function($rootScope, $cookies, $http, User){
    // Sets Auth token if found in cookies and loads user with Username and that.
    if(User.setAuthHeaders()){
        //There was a auth token. Set it to header and load current user.
        User.loadCurrent();
    }
}]);

jarvis_auth.factory('User', ['$rootScope', '$cookies', '$http', '$localStorage', 'Restangular',
    function($rootScope, $cookies, $http, $localStorage, Restangular){
        var User = {
            data : {
                current : false
            },
            loadCurrent : function(){
                // Uses the Auth token header to fetch current so no need to set Auth token or headers.
                Restangular.one('auth/current/').get().then(
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
            getLocalStorage : function(){
                return $localStorage.$default({
                    'auth_token' : undefined
                })
            },
            setAuthToken : function (auth_token){
                var localStorage = User.getLocalStorage();
                User.getLocalStorage().auth_token = auth_token;
                return this;
            },
            getAuthToken : function (){
                var localStorage = User.getLocalStorage();

                if(localStorage.auth_token !== null && localStorage.auth_token !== undefined){
                    return localStorage.auth_token;
                }
                return undefined;
            },
            /*
            * Set Authentication token, defaults to using token found in cookies.
            */
            setAuthHeaders : function (auth_token){
                if(auth_token === undefined){
                    auth_token = User.getAuthToken();
                }

                if(auth_token === undefined){
                    return false;
                }

                $http.defaults.headers.common['Authorization'] = 'Token ' + auth_token;
                return true;
            },
            clearUser : function(){
                User.data.current = false;
                User.getLocalStorage().auth_token = undefined;
                delete $http.defaults.headers.common['Authorization'];
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
                User.setAuthToken(user.auth_token).setAuthHeaders();
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
            // Delete current user
            User.clearUser();
            $rootScope.$broadcast('loggedOut');
            $location.url('/login');
        }
    )
}]);