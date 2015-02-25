# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='humidity',
            field=models.SmallIntegerField(null=True, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='temperature',
            field=models.SmallIntegerField(null=True, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='sensorlog',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
