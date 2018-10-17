# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-30 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_ecshost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='host',
        ),
        migrations.AddField(
            model_name='process',
            name='ecshost',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.EcsHost', verbose_name='所属主机'),
        ),
    ]
