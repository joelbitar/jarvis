from django.db import models
from button.models import Button
from sensor.models import Sensor

#class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;
#class:command;protocol:sartano;model:codeswitch;code:1111011001;method:turnoff;


# a specific sender
class Sender(models.Model):
    house = models.CharField(max_length=256, blank=True, null=True, default=None)
    unit = models.CharField(max_length=256, blank=True, null=True, default=None)
    code = models.CharField(max_length=256, blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)

    last_signal_received = models.DateTimeField(null=True, blank=True, default=None)

    button = models.ForeignKey(Button, null=True, default=None, blank=True, related_name='senders')
    sensor = models.ForeignKey(Sensor, null=True, default=None, blank=True, related_name='senders')

    def get_unit(self):
        if self.button is not None:
            return self.button

        if self.sensor is not None:
            return self.sensor

        return None

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
    event_class = models.CharField(max_length=256, blank=True, null=True, default=None)
    humidity = models.CharField(max_length=256, blank=True, null=True, default=None)
    temp = models.CharField(max_length=256, blank=True, null=True, default=None)

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

    # Propagate this signal to actions and stuff on the unit
    def propagate(self):
        for link in self.get_unit_action_links():
            link.run(signal=self)


    def __str__(self):
        return str(self.pk)
