# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0011_sensor_changed'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorDaily',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('temperature_min', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('temperature_max', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('temperature_avg', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('humidity_min', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('humidity_max', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('humidity_avg', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SensorHourly',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('temperature_min', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('temperature_max', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('temperature_avg', models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True)),
                ('humidity_min', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('humidity_max', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('humidity_avg', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='changed',
        ),
        migrations.AlterField(
            model_name='sensorlog',
            name='temperature',
            field=models.DecimalField(decimal_places=1, max_digits=4, blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='sensorhourly',
            name='sensor',
            field=models.ForeignKey(to='sensor.Sensor', related_name='hourly'),
        ),
        migrations.AddField(
            model_name='sensordaily',
            name='sensor',
            field=models.ForeignKey(to='sensor.Sensor', related_name='daily'),
        ),
    ]
