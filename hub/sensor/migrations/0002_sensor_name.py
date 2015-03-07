# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='name',
            field=models.CharField(max_length=56, default='', blank=True),
        ),
    ]
