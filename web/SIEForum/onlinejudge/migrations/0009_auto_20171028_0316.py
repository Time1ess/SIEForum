# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinejudge', '0008_auto_20171025_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='thread',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='misago_threads.Thread'),
        ),
    ]
