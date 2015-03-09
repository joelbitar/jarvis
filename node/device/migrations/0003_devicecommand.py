# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20150213_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCommand',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('command_name', models.CharField(max_length=56)),
                ('command_data_json', models.TextField(null=True, default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('executed', models.DateTimeField(blank=True, null=True, default=None)),
                ('success', models.NullBooleanField(default=None)),
                ('device', models.ForeignKey(to='device.Device')),
            ],
        ),
    ]
