# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='device_groups',
            new_name='action_device_groups',
        ),
        migrations.RenameField(
            model_name='action',
            old_name='devices',
            new_name='action_devices',
        ),
        migrations.RenameField(
            model_name='action',
            old_name='buttons',
            new_name='trigger_buttons',
        ),
        migrations.RenameField(
            model_name='action',
            old_name='sensors',
            new_name='trigger_sensors',
        ),
    ]
