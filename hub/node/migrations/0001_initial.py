# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=56)),
                ('address', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=256)),
                ('method', models.CharField(max_length=12)),
                ('request_data', models.TextField(blank=True, null=True, default=None)),
                ('response_status_code', models.PositiveSmallIntegerField(blank=True, null=True, default=None)),
                ('response_data', models.TextField(blank=True, null=True, default=None)),
                ('request_sent', models.DateTimeField(auto_now_add=True)),
                ('response_received', models.DateTimeField(blank=True, null=True, default=None)),
            ],
        ),
    ]
