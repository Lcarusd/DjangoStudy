# -*- coding:utf-8 -*-
import django_filters
from blog.models import Article, Record
from blog import models
from taggit.models import Tag


class ArticleFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(name='title', lookup_expr='icontains')
    tags = django_filters.ModelMultipleChoiceFilter(
        name="tag__name",
        queryset=Tag.objects.filter(),
        to_field_name='name',
        # lookup_expr='in',
        label=u'标签分类'
    )

    class Meta:
        model = Article
        fields = ['users', 'status', "title", "tags"]
