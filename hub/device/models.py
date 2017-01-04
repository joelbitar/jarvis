from django.db import models
from django.utils.translation import gettext_lazy as _

from node.models import Node 

from node.communicator import NodeDeviceCommunicator


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

    CATEGORY_LIGHT = 1
    CATEGORY_APPLIANCE = 2
    CATEGORY_CHOICES = (
        (CATEGORY_LIGHT, _('Light')),
        (CATEGORY_APPLIANCE, _('Appliance')),
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
    written_to_conf_on_node = models.BooleanField(default=False)
    learnt_on_node = models.BooleanField(default=False)

    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, null=True, blank=True, default=None)

    # Relations
    node = models.ForeignKey(Node)
    placement = models.ForeignKey('Placement', default=None, null=True, related_name='devices')
    room = models.ForeignKey('Room', default=None, null=True, related_name='devices')

    # String representation
    @property
    def protocol_string(self):
        return dict(self.PROTOCOL_CHOICES).get(self.protocol)

    @property
    def model_string(self):
        return dict(self.MODEL_CHOICES).get(self.model)

    @property
    def is_dimmable(self):
        return self.model in [
            self.MODEL_SELFLEARNING_DIMMER,
        ]

    def get_communicator(self):
        return NodeDeviceCommunicator(device=self)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'device'
        ordering = ('name', )


class DeviceGroup(models.Model):
    SHOW_ONLY_WHEN_CHOICE_OFF = 0
    SHOW_ONLY_WHEN_CHOICE_ON = 1
    SHOW_ONLY_WHEN_CHOICE_ALWAYS_SHOW = 2

    SHOW_ONLY_WHEN_CHOICES = (
        (SHOW_ONLY_WHEN_CHOICE_OFF, _('Off')),
        (SHOW_ONLY_WHEN_CHOICE_ON, _('On')),
        (SHOW_ONLY_WHEN_CHOICE_ALWAYS_SHOW, _('Always')),
    )
    name = models.CharField(max_length=12, help_text=_("'Kitchen', 'Driveway'"))
    show_only_when = models.SmallIntegerField(
        choices=SHOW_ONLY_WHEN_CHOICES,
        default=SHOW_ONLY_WHEN_CHOICE_ALWAYS_SHOW,
        verbose_name=_('Show only when devices are'),
        help_text=_('Will only show this group when the group have selected status')
    )
    devices = models.ManyToManyField(Device)

    @property
    def state(self):
        if self.devices.filter(state__gte=1).count() > 0:
            return 1

        return 0

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'device'
        ordering = ('name', )


class CategoryBaseModel(models.Model):
    name = models.CharField(max_length=18, help_text=_("'First floor', 'attic', 'outside'"))

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'device'
        ordering = ('name', )
        abstract = True


class Placement(CategoryBaseModel):
    # No own properties, JS Depends on it
    pass


class Room(CategoryBaseModel):
    # No own properties, JS Depends on it
    pass
