from django.conf.urls import include, url, patterns

from django.contrib import admin

from rest_framework import routers

from device.views import DeviceViewSet
from device.views import DeviceOptionsView
from device.views import DeviceDetailedView
from device.views import DeviceListShortView
from device.views import DeviceStatesView

from device.views import DeviceCommandOnView
from device.views import DeviceCommandOffView
from device.views import DeviceCommandLearnView
from device.views import DeviceCommandDimView

from device.views import RoomCommandOnView
from device.views import RoomCommandOffView

from device.views import PlacementCommandOnView
from device.views import PlacementCommandOffView

from device.views import DeviceGroupViewSet
from device.views import DeviceGroupCommandOnView
from device.views import DeviceGroupCommandOffView

# Rooms
from device.views import RoomViewSet

# Placements
from device.views import PlacementViewSet

from node.views import NodeViewSet
from node.views import NodeWriteConfView
from node.views import NodeSyncView
from node.views import NodeRestartDaemonView
from node.views import NodeDetailView

from event.views import EventReceiverView
from event.views import RecentSignalsView

from sensor.views import SensorViewSet
from sensor.views import SensorLogView
from sensor.views import SensorsHistoryView
from sensor.views import SensorHistoryView

from forecast.views import ForecastViewSet
from forecast.views import LatestForecastView
from forecast.views import NowForecastView
from forecast.views import ShortForecastView
from forecast.views import DetailedForecastView

from authentication.views import CurrentUserView
from authentication.views import LoginUserView
from authentication.views import LogoutUserView

from progressive.views import ManifestView
from progressive.views import ServiceWorkerView


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
router.register(r'rooms', RoomViewSet)
router.register(r'placements', PlacementViewSet)
router.register(r'groups', DeviceGroupViewSet)
router.register(r'devices/(?P<pk>[0-9]+)/$', device_detail, base_name='devices')
router.register(r'nodes/(?P<pk>[0-9]+)/$', node_detail, base_name='nodes')
router.register(r'sensors', SensorViewSet)
router.register(r'forecasts', ForecastViewSet, base_name='forecasts')
#router.register(r'devices/(?P<pk>[0-9]+)/command/on/$', DeviceCommandOnView.as_view(), base_name='device_command')

rest_patterns = patterns('',
    url(r'^auth/current/', CurrentUserView.as_view(), name='current-user'),
    url(r'^auth/login/', LoginUserView.as_view(), name='login'),
    url(r'^auth/logout/', LogoutUserView.as_view(), name='logout'),
    url(r'^device/options/', DeviceOptionsView.as_view(), name='device-options'),

    url(r'^devices/short/$', DeviceListShortView.as_view(), name="device-list-short"),
    url(r'^devices/states/$', DeviceStatesView.as_view(), name="device-list-states"),
    url(r'^devices/(?P<pk>[0-9]+)/details/$', DeviceDetailedView.as_view(), name="device-extra"),
    url(r'^devices/(?P<pk>[0-9]+)/command/dim/(?P<dimlevel>\d+)/$', DeviceCommandDimView.as_view(), name="device-dim"),
    url(r'^devices/(?P<pk>[0-9]+)/command/on/$', DeviceCommandOnView.as_view(), name="device-on"),
    url(r'^devices/(?P<pk>[0-9]+)/command/off/$', DeviceCommandOffView.as_view(), name="device-off"),
    url(r'^devices/(?P<pk>[0-9]+)/command/learn/$', DeviceCommandLearnView.as_view(), name="device-learn"),

    # Room commands
    url(r'^rooms/(?P<pk>[0-9]+)/command/on/$', RoomCommandOnView.as_view(), name="room-on"),
    url(r'^rooms/(?P<pk>[0-9]+)/command/off/$', RoomCommandOffView.as_view(), name="room-off"),

    # Placement commands
    url(r'^placements/(?P<pk>[0-9]+)/command/on/$', PlacementCommandOnView.as_view(), name="placement-on"),
    url(r'^placements/(?P<pk>[0-9]+)/command/off/$', PlacementCommandOffView.as_view(), name="placement-off"),

    # Group commands
    url(r'^devicegroups/(?P<pk>[0-9]+)/command/on/$', DeviceGroupCommandOnView.as_view(), name="devicegroup-on"),
    url(r'^devicegroups/(?P<pk>[0-9]+)/command/off/$', DeviceGroupCommandOffView.as_view(), name="devicegroup-off"),

    url(r'^nodes/(?P<pk>[0-9]+)/details/$', NodeDetailView.as_view(), name="node-extra"),
    url(r'^nodes/(?P<pk>[0-9]+)/sync/$', NodeSyncView.as_view(), name="node-sync"),
    url(r'^nodes/(?P<pk>[0-9]+)/writeconf/$', NodeWriteConfView.as_view(), name="node-writeconf"),
    url(r'^nodes/(?P<pk>[0-9]+)/restartdaemon/$', NodeRestartDaemonView.as_view(), name="node-restartdaemon"),

    url(r'^event/$', EventReceiverView.as_view(), name="event"),
    url(r'^signals/recent/$', RecentSignalsView.as_view(), name='signals-recent'),

    url(r'^forecast/$', LatestForecastView.as_view(), name="latest-forecast"),
    url(r'^forecast/detailed/$', DetailedForecastView.as_view(), name="forecast-detailed"),
    url(r'^forecast/detailed/(?P<date>.*)$', DetailedForecastView.as_view(), name="forecast-detailed"),
    url(r'^forecast/now/$', NowForecastView.as_view(), name="forecast-now"),
    url(r'^forecast/short/$', ShortForecastView.as_view(), name="forecast-now"),
    url(r'^forecast/now/(?P<date>.*)/$', NowForecastView.as_view(), name="forecast-now"),

    url(r'^sensors/history/$', SensorsHistoryView.as_view(), name='sensors-history'),
    url(r'^sensors/(?P<sensor_pk>\d+)/history/$', SensorHistoryView.as_view(), name='sensor-history'),
    url(r'^sensors/(?P<sensor_pk>\d+)/logs/$', SensorLogView.as_view(), name='sensorlog-list'),

    url(r'^', include(router.urls)),

    # API entrypoints
    url(r'^entrypoint/', include('api.urls'))
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jarvis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^proxy/', include('rest_router.urls')),
    url(r'^api/', include(rest_patterns)), # All REST patterns
    url(r'^admin/', include(admin.site.urls)),
    url(r'^githook/', include('git_hook.urls')),

    url(r'^manifest.json$', ManifestView.as_view(), name='manifest-json'),
    url(r'^service_worker.js$', ServiceWorkerView.as_view(), name='service_worker-js'),

    url(r'^', include('angular.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
