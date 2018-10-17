# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-07 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0010_remove_deploytask_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploytask',
            name='is_upgrade',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='是否已升级'),
        ),
    ]
