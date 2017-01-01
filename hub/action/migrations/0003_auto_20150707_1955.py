# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0002_auto_20150302_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_device_groups',
            field=models.ManyToManyField(to='device.DeviceGroup', blank=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='action_devices',
            field=models.ManyToManyField(to='device.Device', blank=True),
        ),
    ]
