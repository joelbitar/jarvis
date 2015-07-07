# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0006_sensor_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='identifier',
            field=models.CharField(max_length=4, blank=True, default=None, null=True),
        ),
    ]
