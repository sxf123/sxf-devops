# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-28 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0008_deploytask_email_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploytask',
            name='is_sql_exec',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='是否需要执行sql'),
        ),
    ]
