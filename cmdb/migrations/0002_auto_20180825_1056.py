# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-25 10:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cluster',
            options={'permissions': (('scan_cluster', 'Can scan cluster info'), ('resource_manage', 'Can manage 资源'), ('project_manage', 'Can manage 项目')), 'verbose_name': '集群', 'verbose_name_plural': '集群'},
        ),
    ]
