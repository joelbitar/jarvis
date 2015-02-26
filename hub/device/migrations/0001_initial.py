# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('protocol', models.PositiveSmallIntegerField(choices=[(1, 'arctech')])),
                ('name', models.CharField(max_length=56)),
                ('description', models.TextField(blank=True, default='')),
                ('model', models.PositiveSmallIntegerField(choices=[(1, 'codeswitch'), (2, 'bell'), (3, 'selflearning-switch'), (4, 'selflearning-dimmer')])),
                ('controller', models.PositiveIntegerField(blank=True, null=True, default=None)),
                ('devices', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('house', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('unit', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('code', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('system', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('units', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('fade', models.CharField(blank=True, null=True, max_length=12, default=None)),
                ('node_device_pk', models.PositiveIntegerField(blank=True, help_text='PK in the node database', null=True, default=None)),
                ('property_iteration', models.PositiveIntegerField(blank=True, help_text='When auto-generating properties, this is used', null=True, default=None)),
                ('state', models.PositiveIntegerField(blank=True, help_text='Current State', null=True, default=None)),
                ('written_to_conf_on_node', models.BooleanField(default=False)),
                ('learnt_on_node', models.BooleanField(default=False)),
                ('category', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'Light'), (2, 'Appliance')], default=None)),
                ('node', models.ForeignKey(to='node.Node')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text="'Kitchen', 'Driveway'", max_length=12)),
                ('devices', models.ManyToManyField(to='device.Device')),
            ],
        ),
    ]
