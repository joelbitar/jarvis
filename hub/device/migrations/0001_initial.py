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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('protocol', models.PositiveSmallIntegerField(choices=[(1, 'arctech')])),
                ('name', models.CharField(max_length=56)),
                ('description', models.TextField(default='', blank=True)),
                ('model', models.PositiveSmallIntegerField(choices=[(1, 'codeswitch'), (2, 'bell'), (3, 'selflearning-switch'), (4, 'selflearning-dimmer')])),
                ('controller', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('devices', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('house', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('unit', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('code', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('system', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('units', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('fade', models.CharField(max_length=12, default=None, null=True, blank=True)),
                ('node_device_pk', models.PositiveIntegerField(help_text='PK in the node database', default=None, null=True, blank=True)),
                ('node', models.ForeignKey(to='node.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=12, help_text="'Kitchen', 'Driveway'")),
                ('devices', models.ManyToManyField(to='device.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
    ]
