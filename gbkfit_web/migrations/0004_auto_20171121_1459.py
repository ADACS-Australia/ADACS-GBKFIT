# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbkfit_web', '0003_auto_20171120_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psf',
            name='pa',
            field=models.FloatField(default=1),
        ),
    ]
