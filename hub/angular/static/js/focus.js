/**
 * Created by joel on 2016-12-22.
 */

angular.module('ngFocus', []).
    factory('focus', ['$window', function(win){
        var functions = [];
        win.onfocus = function(){
            _.each(functions, function(def){
                var func =  def['executable'];
                func.call(def['scope']);
            })
        };

        return function(func, scope){
            functions.push(
                {
                    executable: func,
                    scope: scope
                }
            )
        };

    }]);
