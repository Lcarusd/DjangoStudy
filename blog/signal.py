# -*- coding:utf-8 -*-

from django.dispatch import Signal, receiver
from django.db.models import signals
from django.db.models.signals import m2m_changed
from blog.models import Article


@receiver(m2m_changed, sender=Article)
def article_edit(sender, **kwags):
    '''接收器'''
    print(sender, kwags)


# 定义信号
# articleSignal = Signal(providing_args=['test'])

# 发送信号
# signals.articleSignal.send(sender=None, allen='test')

'''
method 1：
@recevier装饰器监听一个model，
若model在view函数或serializer函数中被修改，
则接收器接收到信号，执行相应逻辑。

tips：
m2m_changed:当一个模型上的ManyToManyField字段被改变的时候发送信号
那么其他字段被改变是不是需要不同的监听那个方式
'''
