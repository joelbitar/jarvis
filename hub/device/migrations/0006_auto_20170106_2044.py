# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_auto_20170105_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='slug',
            field=models.SlugField(help_text='Common code name', null=True, default=None, max_length=18),
        ),
        migrations.AddField(
            model_name='devicegroup',
            name='slug',
            field=models.SlugField(help_text='Common code name', null=True, default=None, max_length=18),
        ),
        migrations.AddField(
            model_name='placement',
            name='slug',
            field=models.SlugField(help_text='Common code name', null=True, default=None, max_length=18),
        ),
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.SlugField(help_text='Common code name', null=True, default=None, max_length=18),
        ),
    ]
