# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        ('sensor', '0002_auto_20150225_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='senders',
            field=models.ManyToManyField(related_name='sensors', to='event.Sender'),
        ),
    ]
