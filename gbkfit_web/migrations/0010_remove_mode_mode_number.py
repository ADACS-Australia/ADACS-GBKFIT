# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 01:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0009_auto_20171124_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mode',
            name='mode_number',
        ),
    ]
