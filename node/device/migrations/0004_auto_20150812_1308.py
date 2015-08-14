# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_devicecommand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicecommand',
            name='device',
        ),
        migrations.DeleteModel(
            name='DeviceCommand',
        ),
    ]
