# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0005_auto_20150707_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='identifier',
            field=models.CharField(default=None, blank=True, max_length=4),
        ),
    ]
