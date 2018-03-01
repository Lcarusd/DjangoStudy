# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from blog.models import Article, Like

# Register your models here.


admin.site.register(Article)
admin.site.register(Like)
