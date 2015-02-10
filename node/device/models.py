from django.db import models
from device.conf import DeviceConfig
from device.commands import CommandDispatcher


# Create your models here.
class Device(models.Model):
    PROTOCOL_ARCHTEC = 1
    PROTOCOL_CHOICES = (
        (PROTOCOL_ARCHTEC, 'arctech'),
    )

    MODEL_CODESWITCH = 1
    MODEL_BELL = 2
    MODEL_SELFLEARNING_SWITCH = 3
    MODEL_SELFLEARNING_DIMMER = 4
    MODEL_CHOICES = (
        (MODEL_CODESWITCH, 'codeswitch'),
        (MODEL_BELL, 'bell'),
        (MODEL_SELFLEARNING_SWITCH, 'selflearning-switch'),
        (MODEL_SELFLEARNING_DIMMER, 'selflearning-dimmer'),
    )

    protocol = models.PositiveSmallIntegerField(choices=PROTOCOL_CHOICES, default=PROTOCOL_ARCHTEC)
    name = models.CharField(max_length=56)
    description = models.TextField(default='', blank=True)
    model = models.PositiveSmallIntegerField(choices=MODEL_CHOICES)
    controller = models.PositiveIntegerField(null=True, blank=True, default=None)

    # parameters
    devices = models.CharField(max_length=12, null=True, blank=True, default=None)
    house = models.CharField(max_length=12, null=True, blank=True, default=None)
    unit = models.CharField(max_length=12, null=True, blank=True, default=None)
    code = models.CharField(max_length=12, null=True, blank=True, default=None)
    system = models.CharField(max_length=12, null=True, blank=True, default=None)
    units = models.CharField(max_length=12, null=True, blank=True, default=None)
    fade = models.CharField(max_length=12, null=True, blank=True, default=None)

    @property
    def config_id(self):
        return str(self.pk)

    @property
    def protocol_string(self):
        return dict(self.PROTOCOL_CHOICES).get(
            self.protocol
        )

    @property
    def model_string(self):
        return dict(self.MODEL_CHOICES).get(
            self.model
        )

    @property
    def commands(self):
        return CommandDispatcher(device=self)

    def render_config(self):
        return DeviceConfig(
            self
        ).render_device_conf()

    def __unicode__(self):
        return self.protocol_string

    def __str__(self):
        return self.protocol_string



