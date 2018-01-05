# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.Game)
admin.site.register(models.WhiteList)
admin.site.register(models.Version)