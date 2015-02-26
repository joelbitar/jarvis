# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_device_property_iteration'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Light'), (2, 'Appliance')], null=True, blank=True, default=None),
        ),
    ]
