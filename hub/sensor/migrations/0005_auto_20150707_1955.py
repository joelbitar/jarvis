# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0004_auto_20150615_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensorlog',
            options={'ordering': ['-id']},
        ),
    ]
