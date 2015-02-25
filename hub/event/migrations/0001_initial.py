# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('house', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('unit', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('code', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_signal_received', models.DateTimeField(null=True, blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('raw_command', models.TextField()),
                ('protocol', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('house', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('unit', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('model', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('code', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('group', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('method', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('event_class', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('humidity', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('temp', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('sender', models.ForeignKey(default=None, null=True, to='event.Sender', blank=True)),
            ],
        ),
    ]
