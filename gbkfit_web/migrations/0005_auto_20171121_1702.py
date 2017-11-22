# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 06:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0004_auto_20171121_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='scale_z',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='step_z',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
    ]
