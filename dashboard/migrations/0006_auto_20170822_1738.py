# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 08:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20170822_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Project'),
        ),
        migrations.AlterField(
            model_name='solver',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Project'),
        ),
    ]
