# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0006_sensor_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
