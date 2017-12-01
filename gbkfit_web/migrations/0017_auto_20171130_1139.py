# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 00:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0016_auto_20171130_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitter',
            name='epsfcn',
            field=models.FloatField(default=1e-90, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
