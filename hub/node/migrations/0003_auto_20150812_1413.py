# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0002_node_auth_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='api_port',
            field=models.PositiveSmallIntegerField(help_text='Node API port, where the web application is running', default=8000, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='node',
            name='address',
            field=models.CharField(help_text='Host name or IP adress', max_length=128),
        ),
    ]
