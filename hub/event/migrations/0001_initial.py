# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('raw_command', models.TextField()),
                ('protocol', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('house', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('unit', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('model', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('code', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('group', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('method', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('event_class', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('humidity', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('temp', models.CharField(blank=True, max_length=256, null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('house', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('unit', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('code', models.CharField(blank=True, max_length=256, null=True, default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='sender',
            field=models.ForeignKey(blank=True, to='event.Sender', null=True, default=None),
        ),
    ]
