# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('button', '0002_button_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bell',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='BellLog',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='buttonlog',
            name='method',
            field=models.PositiveSmallIntegerField(choices=[(1, 'on'), (2, 'off'), (3, 'learn')]),
        ),
    ]
