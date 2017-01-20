# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_auto_20170109_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='lighttype',
            name='show_only_when',
            field=models.SmallIntegerField(help_text='Will only show this group when the group have selected status', verbose_name='Show only when devices are', default=2, choices=[(0, 'Off'), (1, 'On'), (2, 'Always')]),
        ),
        migrations.AddField(
            model_name='placement',
            name='show_only_when',
            field=models.SmallIntegerField(help_text='Will only show this group when the group have selected status', verbose_name='Show only when devices are', default=2, choices=[(0, 'Off'), (1, 'On'), (2, 'Always')]),
        ),
        migrations.AddField(
            model_name='room',
            name='show_only_when',
            field=models.SmallIntegerField(help_text='Will only show this group when the group have selected status', verbose_name='Show only when devices are', default=2, choices=[(0, 'Off'), (1, 'On'), (2, 'Always')]),
        ),
        migrations.AlterField(
            model_name='devicegroup',
            name='devices',
            field=models.ManyToManyField(to='device.Device', related_name='groups'),
        ),
        migrations.AlterField(
            model_name='devicegroup',
            name='name',
            field=models.CharField(max_length=18, help_text="'First floor', 'attic', 'outside'"),
        ),
    ]
