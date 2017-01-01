# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference_time', models.DateTimeField()),
                ('valid_time', models.DateTimeField()),
                ('t', models.DecimalField(decimal_places=1, verbose_name='Temperature', max_digits=3)),
                ('tcc', models.PositiveSmallIntegerField(verbose_name='Total cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('lcc', models.PositiveSmallIntegerField(verbose_name='Low cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('mcc', models.PositiveSmallIntegerField(verbose_name='Medium cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('hcc', models.PositiveSmallIntegerField(verbose_name='High cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('tstm', models.PositiveSmallIntegerField(verbose_name='Chance of thunder percentage')),
                ('r', models.PositiveSmallIntegerField(verbose_name='Relative humidity')),
                ('vis', models.PositiveIntegerField(verbose_name='Visibility')),
                ('gust', models.DecimalField(decimal_places=1, verbose_name='Gust', max_digits=4)),
                ('pit', models.DecimalField(decimal_places=1, verbose_name='Percipitation intensity total', max_digits=4)),
                ('pis', models.DecimalField(decimal_places=1, verbose_name='Percipitation intensity snow', max_digits=4)),
                ('pcat', models.PositiveSmallIntegerField(verbose_name='Percipitation category', choices=[(0, 'None'), (1, 'Snow'), (2, 'Snow and rain'), (3, 'Rain'), (4, 'Drizzle'), (5, 'Freezing rain'), (6, 'Freezing drizzle')])),
                ('msl', models.DecimalField(decimal_places=1, verbose_name='Air pressure', max_digits=5)),
                ('wd', models.PositiveSmallIntegerField(verbose_name='Wind direction')),
                ('ws', models.DecimalField(decimal_places=1, verbose_name='Wind velocity', max_digits=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForecastLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference_time', models.DateTimeField()),
                ('valid_time', models.DateTimeField()),
                ('t', models.DecimalField(decimal_places=1, verbose_name='Temperature', max_digits=3)),
                ('tcc', models.PositiveSmallIntegerField(verbose_name='Total cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('lcc', models.PositiveSmallIntegerField(verbose_name='Low cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('mcc', models.PositiveSmallIntegerField(verbose_name='Medium cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('hcc', models.PositiveSmallIntegerField(verbose_name='High cloud coverage', help_text='How much cloud coverage, 0-8')),
                ('tstm', models.PositiveSmallIntegerField(verbose_name='Chance of thunder percentage')),
                ('r', models.PositiveSmallIntegerField(verbose_name='Relative humidity')),
                ('vis', models.PositiveIntegerField(verbose_name='Visibility')),
                ('gust', models.DecimalField(decimal_places=1, verbose_name='Gust', max_digits=4)),
                ('pit', models.DecimalField(decimal_places=1, verbose_name='Percipitation intensity total', max_digits=4)),
                ('pis', models.DecimalField(decimal_places=1, verbose_name='Percipitation intensity snow', max_digits=4)),
                ('pcat', models.PositiveSmallIntegerField(verbose_name='Percipitation category', choices=[(0, 'None'), (1, 'Snow'), (2, 'Snow and rain'), (3, 'Rain'), (4, 'Drizzle'), (5, 'Freezing rain'), (6, 'Freezing drizzle')])),
                ('msl', models.DecimalField(decimal_places=1, verbose_name='Air pressure', max_digits=5)),
                ('wd', models.PositiveSmallIntegerField(verbose_name='Wind direction')),
                ('ws', models.DecimalField(decimal_places=1, verbose_name='Wind velocity', max_digits=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('forecast', models.ForeignKey(related_name='logs', to='forecast.Forecast')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
