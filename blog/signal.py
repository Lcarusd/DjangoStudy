# -*- coding:utf-8 -*-
from django.dispatch import Signal, receiver
from blog.models import Article, Record, Tags

# 定义信号
ArticleSignal = Signal(
    providing_args=["user", "article", "before_title", "before_body_text", ])


@receiver(ArticleSignal)
def article_edit(sender, ** kwargs):
    '''接收信号'''
    user = kwargs["user"]
    article = kwargs["article"]
    before_title = kwargs["before_title"]
    before_body_text = kwargs["before_body_text"]
    record = Record(user=user, article=article,
                    before_title=before_title, before_body_text=before_body_text)
    record.save()
