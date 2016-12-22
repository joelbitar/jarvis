/**
 * Created by joel on 2016-12-22.
 */

window.requestAnimFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame;


angular.module('ngFocus', []).
    factory('focus', ['$window', '$rootScope', function(win, rootScope){
        var functions = [], broadcasts = [];
        var lastupdate = new Date();

        /*
        visibly.onVisible(function(){
            _.each(broadcasts, function(def){
                console.log('broadcast');
                
                rootScope.$broadcast(
                    def['signal_name'],
                    def['message']
                )
            });

            // Callbacks
            _.each(functions, function(def){
                var func =  def['executable'];
                func.call(def['scope']);
            })
        });
        */

        (function loop() {
            var now = new Date();

            if ( now - lastupdate > 1000 ) {
                // browser was suspended and did come back to focus
                console.log('updaet');
                _.each(broadcasts, function(def){
                    console.log('broadcast');

                    rootScope.$broadcast(
                        def['signal_name'],
                        def['message']
                    )
                });

                // Callbacks
                _.each(functions, function(def){
                    var func =  def['executable'];
                    func.call(def['scope']);
                })
            }
            lastupdate = now;

            window.requestAnimFrame(loop);
        })();

        return {
            broadcast : function(signal_name, message){
                broadcasts.push(
                    {
                        'signal_name' : signal_name,
                        'message' : message
                    }
                )
            },
            callback : function(func, scope){
                functions.push(
                    {
                        executable: func,
                        scope: scope
                    }
                )
            }
        };

    }]);


