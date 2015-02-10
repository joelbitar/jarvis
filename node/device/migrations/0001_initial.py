# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('protocol', models.PositiveSmallIntegerField(default=1, choices=[(1, 'archtech')])),
                ('name', models.CharField(max_length=56)),
                ('description', models.TextField(default='', blank=True)),
                ('model', models.PositiveSmallIntegerField(choices=[(1, 'codeswitch'), (2, 'bell'), (3, 'selflearning-switch'), (4, 'selflearning-dimmer')])),
                ('controller', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('devices', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('house', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('unit', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('code', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('system', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('units', models.CharField(max_length=12, blank=True, default=None, null=True)),
                ('fade', models.CharField(max_length=12, blank=True, default=None, null=True)),
            ],
        ),
    ]
