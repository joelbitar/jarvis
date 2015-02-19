from django.db import models
from django.utils.translation import gettext_lazy as _

from node.models import Node 

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

    protocol = models.PositiveSmallIntegerField(choices=PROTOCOL_CHOICES)
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

    # Node data
    node_device_pk = models.PositiveIntegerField(null=True, default=None, blank=True, help_text='PK in the node database')

    # Node metadata
    property_iteration = models.PositiveIntegerField(null=True, default=None, blank=True, help_text='When auto-generating properties, this is used')

    # Current state of the device, If null, the device has never changed
    state = models.PositiveIntegerField(null=True, default=None, blank=True, help_text='Current State')

    # Relations
    node = models.ForeignKey(Node)

    # String representation
    @property
    def protocol_string(self):
        return dict(self.PROTOCOL_CHOICES).get(self.protocol)

    @property
    def model_string(self):
        return dict(self.MODEL_CHOICES).get(self.model)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.protocol_string


class Group(models.Model):
    name = models.CharField(max_length=12, help_text=_("'Kitchen', 'Driveway'"))
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    pass


class Button(models.Model):
    pass


class Signal(models.Model):
    """
    Signal such as a email, a chat etc.
    """
    SIGNAL_TYPE_EMAIL = 1
    SIGNAL_TYPE_GOOGLE_TALK = 2

