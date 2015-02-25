from django.db import models
from event.models import Sender


class Button(models.Model):
    """
    Has a relation to a Sender, many senders can be related to one button.
    """
    METHOD_ON = 1
    METHOD_OFF = 2

    created = models.DateTimeField(auto_now_add=True)

    archived = models.BooleanField(default=False)
    senders = models.ManyToManyField(Sender, related_name='units')

    def log(self, signal):
        method_key = {
            'turnon' : Button.METHOD_ON,
            'turnoff' : Button.METHOD_OFF,
        }.get(signal.method)

        if method_key is None:
            raise ValueError('Event method not within choices')

        log_entry = ButtonLog(
            method=method_key
        )

        log_entry.save()

        return log_entry


class ButtonLog(models.Model):
    method = models.PositiveSmallIntegerField(
        choices=(
            (Button.METHOD_ON, 'on'),
            (Button.METHOD_OFF, 'off')
        )
    )
    created = models.DateTimeField(auto_now_add=True)
