# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_auto_20170106_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=18, help_text="'First floor', 'attic', 'outside'")),
                ('slug', models.SlugField(max_length=18, null=True, default=None, help_text='Common code name')),
            ],
            options={
                'abstract': False,
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='device',
            name='light_type',
            field=models.ForeignKey(default=None, to='device.LightType', related_name='devices', null=True, blank=True),
        ),
    ]
