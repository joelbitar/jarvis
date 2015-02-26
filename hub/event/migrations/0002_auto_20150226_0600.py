# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('button', '0003_remove_button_senders'),
        ('sensor', '0004_remove_sensor_senders'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='button',
            field=models.ForeignKey(to='button.Button', related_name='senders', null=True, blank=True, default=None),
        ),
        migrations.AddField(
            model_name='sender',
            name='sensor',
            field=models.ForeignKey(to='sensor.Sensor', related_name='senders', null=True, blank=True, default=None),
        ),
    ]
