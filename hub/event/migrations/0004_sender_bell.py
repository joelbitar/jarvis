# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('button', '0003_auto_20160211_1722'),
        ('event', '0003_sender_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='bell',
            field=models.ForeignKey(related_name='senders', to='button.Bell', default=None, blank=True, null=True),
        ),
    ]
