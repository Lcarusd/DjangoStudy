# -*- coding:utf-8 -*-

from django.dispatch import Signal, receiver
# from django.db.models import signals
from django.db.models.signals import m2m_changed, post_save, post_delete, pre_delete
from blog.models import Article, Record


@receiver(post_save, sender=Article)
def article_edit(sender, instance, created, **kwargs):
    '''接收信号'''
    '''若文章被修改则保存相关修改记录'''
    '''如何获取Article表数据并转存到Record表'''
    print("------------------------------article_edit信号接收成功!----------------------------------")


@receiver(m2m_changed, sender=Article.users.through)
def article_user(sender, instance, created, **kwargs):
    print("------------------------------article_user信号接收成功!----------------------------------")


'''
method 1：
@recevier装饰器监听一个model，
若model在view函数或serializer函数中被修改，
则接收器接收到信号，执行相应逻辑。

tips：
1、m2m_changed:当一个模型上的ManyToManyField字段被改变的时候发送信号
那么其他字段被改变是不是需要不同的监听那个方式
2、若监听到文章被修改，则在修改前将相关数据保存到Record表
'''
