from django.utils.translation import gettext_lazy as _
from django.db import models


class Button(models.Model):
    """
    Has a relation to a Sender, many senders can be related to one button.
    """
    METHOD_ON = 1
    METHOD_OFF = 2
    METHOD_LEARN = 3

    BUTTON_TYPE_BUTTON = 1
    BUTTON_TYPE_MOTION_SENSOR = 2
    BUTTON_TYPE_DOOR_SENSOR = 3

    BUTTON_TYPE_CHOICES = (
        (BUTTON_TYPE_BUTTON, _('Button')),
        (BUTTON_TYPE_MOTION_SENSOR, _('Motion sensor')),
        (BUTTON_TYPE_DOOR_SENSOR, _('Door sensor')),
    )

    name = models.CharField(max_length=56, default='', blank=True)

    created = models.DateTimeField(auto_now_add=True)

    button_type = models.PositiveSmallIntegerField(choices=BUTTON_TYPE_CHOICES, default=BUTTON_TYPE_BUTTON)

    archived = models.BooleanField(default=False)

    def get_method_identifier(self, signal):
        return {
            'turnon' : Button.METHOD_ON,
            'turnoff' : Button.METHOD_OFF,
            'learn' : Button.METHOD_LEARN
        }.get(signal.method)

    def log(self, signal):
        method_key = self.get_method_identifier(signal=signal)

        if method_key is None:
            raise ValueError('Event method not within choices')

        log_entry = ButtonLog(
            method=method_key
        )

        log_entry.save()

        return log_entry

    def __unicode__(self):
        return self.name or '-- unnamed --'

    def __str__(self):
        return self.name or '-- unnamed -- {pk}'.format(pk=self.pk)


class ButtonLog(models.Model):
    method = models.PositiveSmallIntegerField(
        choices=(
            (Button.METHOD_ON, 'on'),
            (Button.METHOD_OFF, 'off'),
            (Button.METHOD_LEARN, 'learn')
        )
    )
    created = models.DateTimeField(auto_now_add=True)
