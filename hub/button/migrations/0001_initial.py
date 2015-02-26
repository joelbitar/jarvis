# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('button_type', models.PositiveSmallIntegerField(choices=[(1, 'Button'), (2, 'Motion sensor'), (3, 'Door sensor')], default=1)),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ButtonLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('method', models.PositiveSmallIntegerField(choices=[(1, 'on'), (2, 'off')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
