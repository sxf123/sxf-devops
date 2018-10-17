# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-07 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0011_deploytask_is_upgrade'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deploytask',
            options={'permissions': (('scan_deploytask', 'Can scan deploytask info'), ('examine_deploytask', 'Can examine deploytask'), ('backspace_deploytask', 'Can backspace deploytask'), ('upgrade_deploytask', 'Can upgrade 升级任务')), 'verbose_name': '升级任务', 'verbose_name_plural': '升级任务'},
        ),
    ]
