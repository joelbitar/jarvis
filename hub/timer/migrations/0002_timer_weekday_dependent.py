# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='weekday_dependent',
            field=models.BooleanField(default=False),
        ),
    ]
