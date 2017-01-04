# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20170104_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicegroup',
            name='show_only_when',
            field=models.SmallIntegerField(verbose_name='Show only when devices are', help_text='Will only show this group when the group have selected status', default=2, choices=[(0, 'Off'), (1, 'On'), (2, 'Always')]),
        ),
    ]
