from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from device.views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)


urlpatterns = [
    # Examples:
    # url(r'^$', 'node.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
