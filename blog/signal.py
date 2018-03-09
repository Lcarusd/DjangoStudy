# -*- coding:utf-8 -*-

from django.db.models import signals
from django.dispatch import receiver

from django.core.signals import request_finished

from django.dispatch import receiver
from blog.models import Article
from django.dispatch import Signal


@receiver(m2m_changed, sender=Article)
def article_edit(sender, **kwags):
    '''接收器'''
    pass

# # 定义信号，向接受者提供 toppings 和 size 参数
# pizza_done = Signal(providing_args=["toppings", "size"])

# # 发送信号
# class PizzaStore(object):
#     def send_pizza(self, toppings, size):
#         pizza_done.send(sender=self.__class__, toppings=toppings, size=size)

# # 监听
# # request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")


# # 手动连接接收器
# # request_finished.connect(my_callback)


# # 断开信号
# Signal.disconnect(receiver=my_callback, sender=Article,)
