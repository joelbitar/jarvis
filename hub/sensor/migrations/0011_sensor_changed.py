# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0010_auto_20170112_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='changed',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 1, 24, 15, 24, 6, 235726, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
