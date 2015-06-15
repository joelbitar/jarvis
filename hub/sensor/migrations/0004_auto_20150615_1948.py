# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0003_auto_20150312_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='temperature',
            field=models.DecimalField(decimal_places=1, null=True, blank=True, default=None, max_digits=3),
        ),
    ]
