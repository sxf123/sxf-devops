# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-17 02:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MavenProj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=255, verbose_name='groupId')),
                ('artifactId', models.CharField(max_length=255, verbose_name='artifactId')),
                ('service_type', models.CharField(max_length=255, verbose_name='service_type')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'maven项目',
                'verbose_name_plural': 'maven项目',
            },
        ),
    ]
