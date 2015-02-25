# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('senders', models.ManyToManyField(related_name='units', to='event.Sender')),
            ],
        ),
        migrations.CreateModel(
            name='ButtonLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('method', models.PositiveSmallIntegerField(choices=[(1, 'on'), (2, 'off')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
