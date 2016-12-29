/**
 * Created by joel on 2016-12-20.
 */

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/service_worker.js', {scope: '/'}).then(function(registration) {
            // Registration was successful
            console.log('ServiceWorker registration successful with scope: ', registration.scope);

            var serviceWorker;
            if (registration.installing) {
                serviceWorker = registration.installing;
            } else if (registration.waiting) {
                serviceWorker = registration.waiting;
            } else if (registration.active) {
                serviceWorker = registration.active;
            }

            if (serviceWorker) {
                console.log("ServiceWorker phase:", serviceWorker.state);

                serviceWorker.addEventListener('statechange', function (e) {
                    console.log("ServiceWorker phase:", e.target.state);
                });
            }
        }).catch(function(err) {
            // registration failed :(
            console.log('ServiceWorker registration failed: ', err);
        });
    });

    self.addEventListener('fetch', function(event) {
        console.log(event.request.url);
        event.respondWith(
            caches.match(event.request).then(function(response) {
                return response || fetch(event.request);
            })
        );
    });
}