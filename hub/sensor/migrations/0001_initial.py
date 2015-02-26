# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('humidity', models.SmallIntegerField(blank=True, null=True, default=None)),
                ('temperature', models.SmallIntegerField(blank=True, null=True, default=None)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('humidity', models.SmallIntegerField()),
                ('temperature', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(related_name='logs', to='sensor.Sensor')),
            ],
        ),
    ]
