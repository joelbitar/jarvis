# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('protocol', models.PositiveSmallIntegerField(choices=[(1, 'arctech')])),
                ('name', models.CharField(max_length=56)),
                ('description', models.TextField(blank=True, default='')),
                ('model', models.PositiveSmallIntegerField(choices=[(1, 'codeswitch'), (2, 'bell'), (3, 'selflearning-switch'), (4, 'selflearning-dimmer')])),
                ('controller', models.PositiveIntegerField(null=True, blank=True, default=None)),
                ('devices', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('house', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('unit', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('code', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('system', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('units', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('fade', models.CharField(null=True, blank=True, max_length=12, default=None)),
                ('node_device_pk', models.PositiveIntegerField(null=True, help_text='PK in the node database', blank=True, default=None)),
                ('state', models.PositiveIntegerField(null=True, help_text='Current State', blank=True, default=None)),
                ('node', models.ForeignKey(to='node.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=12, help_text="'Kitchen', 'Driveway'")),
                ('devices', models.ManyToManyField(to='device.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
    ]
