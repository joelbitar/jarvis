__author__ = 'joel'

from button.models import Button
from sensor.models import Sensor


class BaseJanitor(object):
    def clean(self):
        raise NotImplementedError


class SensorJanitor(object):
    def clean(self):
        Sensor.objects.filter(
            name=''
        ).delete()


class ButtonJanitor(object):
    def clean(self):
        Button.objects.filter(
            name=''
        ).delete()


# The master of all janitors!
class Scruffy(BaseJanitor):
    def clean(self):
        for sub_janitors in [ButtonJanitor, SensorJanitor]:
            sub_janitors().clean()

        return True
