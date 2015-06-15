# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forecast',
            options={'ordering': ['valid_time']},
        ),
        migrations.AlterModelOptions(
            name='forecastlog',
            options={'ordering': ['valid_time']},
        ),
    ]
