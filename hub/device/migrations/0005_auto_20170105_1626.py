# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('device', '0004_devicegroup_show_only_when'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 5, 15, 26, 52, 351508, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='placement',
            field=models.ForeignKey(null=True, to='device.Placement', related_name='devices', default=None),
        ),
        migrations.AlterField(
            model_name='device',
            name='room',
            field=models.ForeignKey(null=True, to='device.Room', related_name='devices', default=None),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='device',
            field=models.ForeignKey(to='device.Device', related_name='logs'),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, default=None),
        ),
    ]
