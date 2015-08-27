# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0003_auto_20150707_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='block_sending',
            field=models.BooleanField(help_text='If set to True, we will NOT send the signal. but we will pretend we did.', default=False),
        ),
    ]
