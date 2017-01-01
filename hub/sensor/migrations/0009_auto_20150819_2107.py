# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0008_auto_20150814_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='temperature',
            field=models.DecimalField(max_digits=4, blank=True, null=True, decimal_places=1, default=None),
        ),
    ]
