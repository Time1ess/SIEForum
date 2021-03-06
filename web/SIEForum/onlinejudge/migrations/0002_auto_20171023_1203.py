# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('onlinejudge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='rank_type',
        ),
        migrations.AddField(
            model_name='problem',
            name='order_type',
            field=models.CharField(choices=[('low', 'Lower score first'), ('high', 'Higher score first')], default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
