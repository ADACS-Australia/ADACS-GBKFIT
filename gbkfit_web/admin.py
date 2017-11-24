# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from gbkfit_web import models

# Register your models here.
admin.site.register(models.Job)
admin.site.register(models.User)
admin.site.register(models.DataSet)
admin.site.register(models.Verification)
admin.site.register(models.ModeImage)
admin.site.register(models.ResultFile)
