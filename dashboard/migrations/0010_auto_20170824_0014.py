# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20170823_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solver',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='solver',
            name='file_path2',
        ),
        migrations.AddField(
            model_name='solver',
            name='solver_file',
            field=models.FileField(blank=True, max_length=200, upload_to='solver'),
        ),
    ]