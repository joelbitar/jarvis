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
            name='property_iteration',
            field=models.PositiveIntegerField(default=None, blank=True, help_text='When auto-generating properties, this is used', null=True),
        ),
    ]
