# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0007_auto_20171008_0131'),
        ('onlinejudge', '0003_auto_20171023_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='thread',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='misago_threads.Thread'),
            preserve_default=False,
        ),
    ]
