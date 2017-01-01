# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_sensor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlog',
            name='humidity',
            field=models.SmallIntegerField(blank=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='sensorlog',
            name='temperature',
            field=models.SmallIntegerField(blank=True, null=True, default=None),
        ),
    ]
