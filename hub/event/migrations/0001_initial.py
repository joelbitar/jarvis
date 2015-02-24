# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('received', models.DateTimeField(auto_now_add=True)),
                ('raw_command', models.TextField()),
                ('protocol', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('house', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('unit', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('model', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('code', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('group', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('method', models.CharField(null=True, blank=True, max_length=256, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('house', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('unit', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('code', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, to='event.Sender', default=None),
        ),
    ]
