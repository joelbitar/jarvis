# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        ('button', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='button',
            name='senders',
        ),
        migrations.AddField(
            model_name='button',
            name='senders',
            field=models.ManyToManyField(related_name='buttons', to='event.Sender'),
        ),
    ]
