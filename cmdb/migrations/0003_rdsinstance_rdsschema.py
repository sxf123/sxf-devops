# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-27 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20180825_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='RdsInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_name', models.CharField(max_length=255, verbose_name='实例名称')),
                ('instance_url', models.CharField(max_length=255, verbose_name='实例地址')),
                ('db_type', models.CharField(max_length=255, null=True, verbose_name='数据库类型')),
                ('instance_desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='实例描述')),
            ],
            options={
                'verbose_name': 'rds实例',
                'verbose_name_plural': 'rds实例',
                'permissions': (('scan_rdsinstance', 'Can scan RDS实例'),),
            },
        ),
        migrations.CreateModel(
            name='RdsSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(blank=True, max_length=255, verbose_name='schema名称')),
                ('schema_desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='schema描述')),
                ('rdsinstanc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.RdsInstance', verbose_name='rds实例')),
            ],
            options={
                'verbose_name': '数据库schema',
                'verbose_name_plural': '数据库schema',
                'permissions': (('scan_rdsschema', 'Can scan rdsschema'),),
            },
        ),
    ]
