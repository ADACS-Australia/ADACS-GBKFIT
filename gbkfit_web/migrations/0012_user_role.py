# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-28 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0011_mode_mode_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='user', max_length=5),
        ),
    ]