# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('button', '0003_remove_button_senders'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='button_type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'Button'), (2, 'Motion sensor'), (3, 'Door sensor')]),
        ),
    ]
