# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0012_auto_20170130_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordaily',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 2, 3, 5, 11, 58, 704734, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensorhourly',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 2, 3, 5, 12, 3, 462750, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
