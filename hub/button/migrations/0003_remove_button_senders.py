# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('button', '0002_auto_20150225_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='button',
            name='senders',
        ),
    ]
