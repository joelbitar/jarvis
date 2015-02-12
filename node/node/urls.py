from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from device.views import DeviceViewSet

device_detail = DeviceViewSet.as_view({
    'get': 'retrieve',
})

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'devices/(?P<pk>[0-9]+)/$', device_detail, base_name='devices')


urlpatterns = [
    # Examples:
    # url(r'^$', 'node.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
