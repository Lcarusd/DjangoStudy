# -*- coding:utf-8 -*-
from django.dispatch import Signal, receiver
from django.db.models.signals import m2m_changed, post_save, post_delete, pre_delete
from blog.models import Article, Record

# 定义信号
ArticleSignal = Signal(providing_args=["rr", ])


@receiver(post_save, sender=Article)
def article_edit(sender, instance, ** kwargs):
    '''接收信号'''
    print("--------------------------article_edit信号接收成功!--------------------------")
    print(sender,)
    print("--------------------------article_edit信号接收成功!--------------------------")
    print(instance,)
    print("--------------------------article_edit信号接收成功!--------------------------")
    print(kwargs)
    print("--------------------------article_edit信号接收成功!--------------------------")

    # a = instance.title
    # # user = instance.users
    # user = kwargs.get("user")
    # print(user)
    # record = Record(user=user, article=instance,
    #                 before_title=a, before_body_text=instance.body_text)
    # record.save()

# @receiver(m2m_changed, sender=Article.users.through)
# def article_user(sender, instance, created, **kwargs):
#     print("--------------------------article_user信号接收成功!--------------------------")


# 如果有作者编辑、
# 则通过signals记录 包含编辑人、编辑文章、时间、编辑前和编辑后的文章、标题、tags(有现成的库)
