{% load static %}{% load version_tags %}var CACHE_NAME = "jarvis-{% version_number %}", urlsToCache = [
    '/',
    {% for resource in resources %}
    '{% static resource %}{% version_extension %}',{% endfor %}
    {% for resource in non_versioned_resources %}
    '{% static resource %}',{% endfor %}
];

self.addEventListener('install', function(event) {
    // Perform install steps
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.match(event.request).then(function (cache_entry) {
                return cache_entry || fetch(event.request).then(
                        function(response) {
                            var should_cache = false;
                            // todo: rules for calls that should be cached and set should_cache to true.

                            if(should_cache){
                                cache.put(event.request, response.clone());
                            }
                            return response;
                        }
                    );
            });
        })
    );
});