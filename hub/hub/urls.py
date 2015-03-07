from django.conf.urls import include, url, patterns
from django.contrib import admin

from rest_framework import routers

from device.views import DeviceViewSet
from device.views import RestartDaemonView
from device.views import WriteConfigView
from device.views import DeviceOptionsView

from device.views import DeviceCommandOnView
from device.views import DeviceCommandOffView
from device.views import DeviceCommandLearnView

from node.views import NodeViewSet
from node.views import NodeWriteConfView
from node.views import NodeRestartDaemonView

from event.views import EventReceiverView

from sensor.views import SensorViewSet


from django.conf import settings
from django.conf.urls.static import static

node_detail = NodeViewSet.as_view({
        'get': 'retrieve',
})

device_detail = DeviceViewSet.as_view({
        'get': 'retrieve',
})

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'nodes', NodeViewSet)
router.register(r'devices/(?P<pk>[0-9]+)/$', device_detail, base_name='devices')
router.register(r'nodes/(?P<pk>[0-9]+)/$', node_detail, base_name='nodes')
router.register(r'sensors', SensorViewSet)
#router.register(r'devices/(?P<pk>[0-9]+)/command/on/$', DeviceCommandOnView.as_view(), base_name='device_command')

rest_patterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^device/options/', DeviceOptionsView.as_view(), name='device-options'),
    url(r'^devices/(?P<pk>[0-9]+)/command/on/$', DeviceCommandOnView.as_view(), name="device-on"),
    url(r'^devices/(?P<pk>[0-9]+)/command/off/$', DeviceCommandOffView.as_view(), name="device-off"),
    url(r'^devices/(?P<pk>[0-9]+)/command/learn/$', DeviceCommandLearnView.as_view(), name="device-learn"),
    url(r'^nodes/(?P<pk>[0-9]+)/writeconf/$', NodeWriteConfView.as_view(), name="node-writeconf"),
    url(r'^nodes/(?P<pk>[0-9]+)/restartdaemon/$', NodeRestartDaemonView.as_view(), name="node-restartdaemon"),
    url(r'^event/$', EventReceiverView.as_view(), name="event"),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jarvis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('angular.urls')),
    url(r'^proxy/', include('rest_router.urls')),
    url(r'^api/', include(rest_patterns)), # All REST patterns
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
