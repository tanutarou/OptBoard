# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 15:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20170824_0014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solver',
            old_name='params',
            new_name='params_info',
        ),
    ]
