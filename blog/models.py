# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Article(models.Model):
    '''文章表'''

    STATUS_CHOICES = (
        ('PUBLIC', u'公开文章'),
        ('HIDE', u'隐藏文章'),
    )

    user = models.ForeignKey(User, related_name='article', verbose_name=u'作者')
    title = models.CharField(u'文章标题', max_length=255)
    body_text = models.TextField(u'文章内容')
    like_count = models.IntegerField(u'文章被点赞的次数', default=0)
    status = models.CharField(u'文章状态', max_length=10,
                              choices=STATUS_CHOICES, default='PUBLIC')

    def __unicode__(self):
        return self.title


class Like(models.Model):
    '''点赞表'''
    user = models.ForeignKey(User)  # 用户
    article = models.ForeignKey(Article)    # 文章
