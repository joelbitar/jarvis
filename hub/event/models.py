from django.db import models
from button.models import Button
from sensor.models import Sensor
from button.models import Bell

#class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;
#class:command;protocol:sartano;model:codeswitch;code:1111011001;method:turnoff;


# a specific sender
class Sender(models.Model):
    UNIT_BUTTON = 1
    UNIT_SENSOR = 2
    UNIT_BELL = 3

    house = models.CharField(max_length=256, blank=True, null=True, default=None)
    unit = models.CharField(max_length=256, blank=True, null=True, default=None)
    code = models.CharField(max_length=256, blank=True, null=True, default=None)
    identifier = models.CharField(max_length=256, blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)

    last_signal_received = models.DateTimeField(null=True, blank=True, default=None)

    button = models.ForeignKey(Button, null=True, default=None, blank=True, related_name='senders')
    sensor = models.ForeignKey(Sensor, null=True, default=None, blank=True, related_name='senders')
    bell = models.ForeignKey(Bell, null=True, default=None, blank=True, related_name='senders')

    def get_unit(self):
        if self.get_unit_type() is self.UNIT_BUTTON:
            return self.button

        if self.get_unit_type() is self.UNIT_SENSOR:
            return self.sensor

        if self.get_unit_type() is self.UNIT_BELL:
            return self.bell

        return None

    def get_unit_type(self):
        if self.button is not None:
            return self.UNIT_BUTTON

        if self.sensor is not None:
            return self.UNIT_SENSOR

        if self.bell is not None:
            return self.UNIT_BELL

        return None

    def get_unit_type_string(self):
        return {
            self.UNIT_BUTTON: 'button',
            self.UNIT_SENSOR: 'sensor',
        }.get(self.get_unit_type(), None)

    def get_unit_name(self):
        try:
            return self.get_unit().name
        except AttributeError:
            return None

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = None

        if not self.unit:
            self.unit = None

        if not self.identifier:
            self.identifier = None

        if not self.house:
            self.house = None

        return super(Sender, self).save(*args, **kwargs)

    def __str__(self):
        return 'house: {sender.house}, unit: {sender.unit}, code: {sender.code}, last signal: {sender.last_signal_received}'.format(
            sender=self
        )


# The signal, every signal event that comes through the tellstick is recorded here!
class Signal(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    raw_command = models.TextField()

    protocol = models.CharField(max_length=256, blank=True, null=True, default=None)
    house = models.CharField(max_length=256, blank=True, null=True, default=None)
    unit = models.CharField(max_length=256, blank=True, null=True, default=None)
    model = models.CharField(max_length=256, blank=True, null=True, default=None)
    code = models.CharField(max_length=256, blank=True, null=True, default=None)
    group = models.CharField(max_length=256, blank=True, null=True, default=None)
    method = models.CharField(max_length=256, blank=True, null=True, default=None)
    # named 'class' in event.
    event_class = models.CharField(max_length=256, blank=True, null=True, default=None)
    humidity = models.CharField(max_length=256, blank=True, null=True, default=None)
    temp = models.CharField(max_length=256, blank=True, null=True, default=None)
    # named 'id' in events.
    identifier = models.CharField(max_length=8, blank=True, null=True, default=None)

    sender = models.ForeignKey(Sender, null=True, blank=True, default=None)

    def get_unit(self):
        return self.sender.get_unit()

    # Get links between the unit and the action
    def get_unit_action_links(self):
        unit = self.get_unit()
        if isinstance(unit, Button):
            return unit.actionbutton_set.all()
        if isinstance(unit, Sensor):
            return unit.actionsensor_set.all()
        if isinstance(unit, Bell):
            return unit.actions()

        print('unit', unit)

    # Propagate this signal to actions and stuff on the unit
    def propagate(self):
        for link in self.get_unit_action_links():
            link.run(signal=self)


    def __str__(self):
        return str(self.pk)
