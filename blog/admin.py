# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from blog.models import Article, Like

# Register your models here.

# 在后台注册Article、Like模块
admin.site.register(Article)
admin.site.register(Like)
