# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-14 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0013_deploytask_belong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploytask',
            name='is_sql_exec',
            field=models.CharField(blank=True, default='no', max_length=255, null=True, verbose_name='是否需要执行sql'),
        ),
    ]
