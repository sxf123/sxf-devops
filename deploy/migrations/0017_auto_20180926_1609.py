# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-26 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0016_auto_20180918_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploytask',
            name='upgrade_success_time',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='升级成功时间'),
        ),
        migrations.AddField(
            model_name='deploytask',
            name='upgrade_time',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='升级操作时间'),
        ),
    ]
