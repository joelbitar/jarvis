from device.models import Room
from device.models import Device
from device.models import Placement
from device.models import DeviceGroup
from device.models import LightType

from api.vendors.api_ai import ApiAiResponse


class ActionBase(object):
    def __init__(self, vendor_name):
        self.__vendor_name = vendor_name

    def set_vendor_name(self, vendor_name):
        self.__vendor_name = vendor_name

    @property
    def vendor_name(self):
        return self.__vendor_name

    def get_response_object(self, *args, **kwargs):
        cls = {
            'api_ai': ApiAiResponse
        }.get(
            self.vendor_name,
            None
        )

        obj = cls(*args, **kwargs)

        return obj


    def get_location(self, slug):
        filters = {
            'slug': slug
        }

        for model in [Room, Placement, DeviceGroup, Device]:
            try:
                return model.objects.get(**filters)
            except model.DoesNotExist:
                pass

    def get_light_type(self, slug):
        try:
            return LightType.objects.get(
                slug=slug
            )
        except LightType.DoesNotExist:
            return None

    def run(self, properties):
        raise NotImplementedError()

