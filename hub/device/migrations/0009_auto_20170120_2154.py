# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0008_auto_20170117_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicegroup',
            name='show_only_when',
            field=models.SmallIntegerField(verbose_name='Show only when devices are', choices=[(0, 'Off'), (1, 'On'), (2, 'Always'), (3, 'Never')], help_text='Will only show this group when the group have selected status', default=2),
        ),
        migrations.AlterField(
            model_name='lighttype',
            name='show_only_when',
            field=models.SmallIntegerField(verbose_name='Show only when devices are', choices=[(0, 'Off'), (1, 'On'), (2, 'Always'), (3, 'Never')], help_text='Will only show this group when the group have selected status', default=2),
        ),
        migrations.AlterField(
            model_name='placement',
            name='show_only_when',
            field=models.SmallIntegerField(verbose_name='Show only when devices are', choices=[(0, 'Off'), (1, 'On'), (2, 'Always'), (3, 'Never')], help_text='Will only show this group when the group have selected status', default=2),
        ),
        migrations.AlterField(
            model_name='room',
            name='show_only_when',
            field=models.SmallIntegerField(verbose_name='Show only when devices are', choices=[(0, 'Off'), (1, 'On'), (2, 'Always'), (3, 'Never')], help_text='Will only show this group when the group have selected status', default=2),
        ),
    ]
