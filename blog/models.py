# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from django.dispatch import Signal

# Create your models here.


class Tags(models.Model):
    '''标签表'''
    name = models.CharField(u'标签名', max_length=50,)
    count = models.IntegerField(u'标签使用频次', default=0)


class Article(models.Model):
    '''文章表'''
    STATUS_CHOICES = (
        ('PUBLIC', u'公开文章'),
        ('HIDE', u'隐藏文章'),
    )

    users = models.ManyToManyField(
        User, related_name='article', verbose_name=u'作者')
    title = models.CharField(u'文章标题', max_length=255)
    body_text = models.TextField(u'文章内容')
    like_count = models.IntegerField(u'文章被点赞的次数', default=0)
    status = models.CharField(u'文章状态', max_length=10,
                              choices=STATUS_CHOICES, default='PUBLIC')
    # tags = models.ForeignKey(Tags,)
    tag = TaggableManager()

    def __unicode__(self):
        return self.title


class Like(models.Model):
    '''点赞表'''
    user = models.ForeignKey(User)  # 用户
    article = models.ForeignKey(Article)    # 文章


class Record(models.Model):
    '''记录表'''
    user = models.ForeignKey(User, verbose_name=u'编辑人')  # 用户
    article = models.ForeignKey(Article, verbose_name=u'编辑文章')
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name=u'编辑时间')
    before_title = models.CharField(u'编辑前标题', max_length=255)
    before_body_text = models.TextField(u'编辑前内容')
    tags = models.ManyToManyField(Tags, verbose_name=u'关联tags表')
