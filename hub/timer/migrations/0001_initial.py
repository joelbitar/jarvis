# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dow_monday', models.BooleanField(default=False, verbose_name='monday', help_text='Monday')),
                ('dow_tuesday', models.BooleanField(default=False, verbose_name='tuesday', help_text='Tuesday')),
                ('dow_wednesday', models.BooleanField(default=False, verbose_name='wednesday', help_text='Wednesday')),
                ('dow_thursday', models.BooleanField(default=False, verbose_name='thursday', help_text='Thursday')),
                ('dow_friday', models.BooleanField(default=False, verbose_name='friday', help_text='Friday')),
                ('dow_saturday', models.BooleanField(default=False, verbose_name='saturday', help_text='Saturday')),
                ('dow_sunday', models.BooleanField(default=False, verbose_name='sunday', help_text='Sunday')),
            ],
        ),
        migrations.CreateModel(
            name='TimerTimeIntervals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('timer', models.ForeignKey(to='timer.Timer', related_name='intervals')),
            ],
        ),
    ]
