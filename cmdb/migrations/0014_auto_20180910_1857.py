# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-09-10 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0013_auto_20180831_1244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cluster',
            options={'permissions': (('scan_cluster', 'Can scan cluster info'), ('resource_manage', 'Can manage 资源'), ('project_manage', 'Can manage 项目'), ('ldap_add', 'Can add LDAP用户')), 'verbose_name': '集群', 'verbose_name_plural': '集群'},
        ),
    ]
