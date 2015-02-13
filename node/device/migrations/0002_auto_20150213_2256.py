# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='written_to_conf',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='device',
            name='model',
            field=models.CharField(max_length=56),
        ),
        migrations.AlterField(
            model_name='device',
            name='protocol',
            field=models.CharField(max_length=56),
        ),
    ]
