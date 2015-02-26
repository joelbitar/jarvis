# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
        ('device', '0001_initial'),
        ('button', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ActionButton',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('command_filter', models.PositiveSmallIntegerField(help_text='What signals are passed through', choices=[(1, 'No filter, sends all through'), (2, 'Only allow ON commands'), (3, 'Only allow OFF commands')], default=1)),
                ('action', models.ForeignKey(to='action.Action')),
                ('button', models.ForeignKey(to='button.Button')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActionSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('action', models.ForeignKey(to='action.Action')),
                ('sensor', models.ForeignKey(to='sensor.Sensor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='action',
            name='buttons',
            field=models.ManyToManyField(related_name='actions', through='action.ActionButton', to='button.Button'),
        ),
        migrations.AddField(
            model_name='action',
            name='device_groups',
            field=models.ManyToManyField(to='device.DeviceGroup'),
        ),
        migrations.AddField(
            model_name='action',
            name='devices',
            field=models.ManyToManyField(to='device.Device'),
        ),
        migrations.AddField(
            model_name='action',
            name='sensors',
            field=models.ManyToManyField(related_name='actions', through='action.ActionSensor', to='sensor.Sensor'),
        ),
    ]
