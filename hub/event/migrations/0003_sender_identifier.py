# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_signal_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='identifier',
            field=models.CharField(blank=True, max_length=256, default=None, null=True),
        ),
    ]
