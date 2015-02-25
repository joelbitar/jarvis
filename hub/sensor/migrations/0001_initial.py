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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_created=True)),
                ('humidity', models.SmallIntegerField()),
                ('temperature', models.SmallIntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SensorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_created=True)),
                ('humidity', models.SmallIntegerField()),
                ('temperature', models.SmallIntegerField()),
                ('sensor', models.ForeignKey(related_name='logs', to='sensor.Sensor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
