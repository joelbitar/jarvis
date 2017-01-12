# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(help_text="'First floor', 'attic', 'outside'", max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(help_text='Name of room', max_length=12)),
            ],
        ),
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='device',
            name='placement',
            field=models.ForeignKey(default=None, to='device.Placement', null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='room',
            field=models.ForeignKey(default=None, to='device.Room', null=True),
        ),
    ]
