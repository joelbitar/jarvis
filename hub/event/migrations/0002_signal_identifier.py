# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signal',
            name='identifier',
            field=models.CharField(default=None, blank=True, max_length=8, null=True),
        ),
    ]
