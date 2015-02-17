# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('method', models.CharField(max_length=12)),
                ('request_data', models.TextField(null=True, blank=True, default=None)),
                ('response_status_code', models.PositiveSmallIntegerField(null=True, blank=True, default=None)),
                ('response_data', models.TextField(null=True, blank=True, default=None)),
                ('request_sent', models.DateTimeField(auto_now_add=True)),
                ('response_received', models.DateTimeField(null=True, blank=True, default=None)),
            ],
        ),
    ]
