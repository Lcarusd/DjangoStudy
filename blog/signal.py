# -*- coding:utf-8 -*-
from django.dispatch import Signal, receiver
from django.db.models.signals import m2m_changed, post_save, post_delete, pre_delete
from blog.models import Article, Record

# 定义信号
ArticleSignal = Signal(providing_args=["rr", ])


@receiver(post_save, sender=Article)
def article_edit(sender, instance, **kwargs):
    '''接收信号'''
    print("--------------------------article_edit信号接收成功!--------------------------")


@receiver(m2m_changed, sender=Article.users.through)
def article_user(sender, instance, created, **kwargs):
    print("--------------------------article_user信号接收成功!--------------------------")
