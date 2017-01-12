# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20170103_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicegroup',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='placement',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='placement',
            name='name',
            field=models.CharField(help_text="'First floor', 'attic', 'outside'", max_length=18),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(help_text="'First floor', 'attic', 'outside'", max_length=18),
        ),
    ]
