# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_auto_20170109_1446'),
        ('sensor', '0009_auto_20150819_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensor',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='sensor',
            name='placement',
            field=models.ForeignKey(default=None, null=True, blank=True, related_name='sensors', to='device.Placement'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='room',
            field=models.ForeignKey(default=None, null=True, blank=True, related_name='sensors', to='device.Room'),
        ),
    ]
