# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 20:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0002_auto_20171020_0346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fitter',
            old_name='_is',
            new_name='multinest_is',
        ),
    ]
