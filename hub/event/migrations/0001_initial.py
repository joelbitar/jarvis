# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
        ('button', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('house', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('unit', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('code', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_signal_received', models.DateTimeField(blank=True, null=True, default=None)),
                ('button', models.ForeignKey(blank=True, related_name='senders', to='button.Button', null=True, default=None)),
                ('sensor', models.ForeignKey(blank=True, related_name='senders', to='sensor.Sensor', null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('raw_command', models.TextField()),
                ('protocol', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('house', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('unit', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('model', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('code', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('group', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('method', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('event_class', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('humidity', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('temp', models.CharField(blank=True, null=True, max_length=256, default=None)),
                ('sender', models.ForeignKey(blank=True, to='event.Sender', null=True, default=None)),
            ],
        ),
    ]
