from django.db import models
from django.utils.translation import gettext_lazy as _


class RoomGroup(models.Model):
    name = models.CharField(max_length=55, help_text=_("'First floor', 'Basement', 'Hallways', 'Outside'"))


class Room(models.Model):
    name = models.CharField(max_length=12, help_text=_("'Kitchen', 'Driveway'"))
    room_group = models.ManyToManyField(RoomGroup)


class Device(models.Model):
    """
    Receiver device, such as a
    """
    DEVICE_TYPE_DIMMER = 1
    DEVICE_TYPE_SWITCH = 2
    DEVICE_TYPE_BELL = 3

    DEVICE_TYPES = (
        (DEVICE_TYPE_DIMMER, _('Dimmer')),
        (DEVICE_TYPE_SWITCH, _('Switch')),
        (DEVICE_TYPE_BELL, _('Bell')),
    )

    BROADCASTER_TELLSTICK = 1
    BROADCASTER_CHOICES = (
        (BROADCASTER_TELLSTICK, _('Tellstick')),
    )

    broadcaster_data = models.CharField(max_length=255, db_index=True, unique=True)
    name = models.CharField(max_length=55)
    room = models.ForeignKey(Room)
    broadcaster = models.PositiveSmallIntegerField(choices=BROADCASTER_CHOICES, default=BROADCASTER_TELLSTICK)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPES)


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
