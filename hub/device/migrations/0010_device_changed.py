# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0009_auto_20170120_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='changed',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 1, 24, 15, 24, 1, 201944, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
