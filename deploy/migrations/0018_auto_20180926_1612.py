# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-26 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0017_auto_20180926_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploytask',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='工单创建时间'),
        ),
    ]