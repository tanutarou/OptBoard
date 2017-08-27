# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 13:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Optimizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file_path', models.FilePathField()),
                ('registered_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OptResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('params', models.TextField()),
                ('eval_val', models.FloatField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.TextField()),
                ('optimizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Optimizer')),
            ],
        ),
    ]