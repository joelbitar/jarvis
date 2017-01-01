# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0003_auto_20150812_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='api_port',
            field=models.PositiveSmallIntegerField(help_text='Node API port, where the web application is running'),
        ),
    ]
