# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0007_sensor_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='active',
            field=models.BooleanField(help_text='If we should bother with the sensor', default=False),
        ),
    ]
