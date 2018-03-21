# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import serializers
from blog.models import Article, Like, Record, Tags, User

from django.dispatch import Signal
from blog.signal import ArticleSignal

import jieba
import jieba.analyse
import itertools
from collections import Counter


class UserLoginSerializer(serializers.Serializer):
    '''用户登录序列化'''
    username = serializers.CharField(label=u'用户名')
    password = serializers.CharField(label=u'密码', min_length=6)

    def validate(self, data):
        '''验证数据'''
        # 用户名校验
        user = User.objects.filter(username__iexact=data['username']).first()
        # 密码校验
        if user and user.check_password(data['password']):
            login(self.context['request'], user)
        else:
            raise serializers.ValidationError(u'登录失败')
        return data


class UserSerializer(serializers.ModelSerializer):
    '''用户列表、详情页序列化'''
    class Meta:
        model = User
        # 列表展示的字段、创建时需要的字段
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        # 密码是通过set_password生成hash，进一步再保存
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ArticleListSerializer(serializers.ModelSerializer):
    '''文章列表序列化'''
    like_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        tags = obj.tag.names()
        tags = [tag for tag in tags]
        return tags

    def get_like_users(self, obj):
        data = list(Like.objects.filter(article=obj).order_by(
            '-id').values_list('user__username', flat=True))
        return data

    def get_users(self, obj):
        return obj.users.all().values_list(
            'username', flat=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'users', 'like_count', 'like_users', 'tags')


class ArticleSerializer(serializers.ModelSerializer):
    '''文章创建更新序列化'''
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        return obj.users.all().values_list(
            'username', flat=True)

    def create(self, validated_data):
        instance = super(ArticleSerializer, self).create(validated_data)
        instance.users.add(self.context['request'].user)  # 获取编辑作者
        return instance

    def update(self, instance, validated_data):
        body_text = validated_data.get('body_text', instance.body_text)
        tags = jieba.analyse.extract_tags(body_text, topK=3)
        for t in tags:
            instance.tag.add(t)

        queryset = Article.objects.all()
        lists = [i.tag.names() for i in queryset]
        tags_list = list(itertools.chain.from_iterable(lists))
        for t in tags_list:
            tag = Tags.objects.filter(name__exact=t).first()
            if tag:
                tag.count = tag.count + 1
            else:
                tag = Tags(name=t, count=1)
            tag.save()

        instance.title = validated_data['title']
        instance.body_text = validated_data['body_text']
        instance.users.add(self.context['request'].user, )
        ArticleSignal.send(
            sender=Article, user=self.context['request'].user,
            article=instance, before_title=validated_data['title'],
            before_body_text=validated_data['body_text'])
        instance.save()
        return instance

    class Meta:
        model = Article
        fields = ('id', 'users', 'title', 'body_text', 'status', )


class LikeSerializer(serializers.ModelSerializer):
    '''用户点赞'''

    def validate(self, data):

        like = Like.objects.filter(
            article=data['article'], user=self.context['request'].user).first()
        if data['article'].status == u'HIDE':
            raise serializers.ValidationError(u'文章未找到')
        elif like:
            raise serializers.ValidationError(u'已经点过赞了')
        # 向data中追加了user以供create时使用
        data['user'] = self.context['request'].user
        return data

    def create(self, validated_data):
        instance = super(LikeSerializer, self).create(validated_data)
        # 防止top脏读、脏写
        instance.article.like_count = F('like_count') + 1
        instance.article.save()
        return instance

    class Meta:
        model = Like
        fields = ('article', )


class RecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'user', 'article', 'update_datetime',
                  'before_title', 'before_body_text')


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'count')


class DiffSerializer(serializers.Serializer):
    record1 = serializers.ChoiceField(choices=Record.objects.all())
    record2 = serializers.ChoiceField(
        choices=Record.objects.all(), allow_null=True)

    def diff(self):
        data = self.validated_data
        record1 = data['record1']
        record2 = data['record2']
        if record2:
            if record1.before_title != record2.before_title:
                return False
            if record1.before_body_text != record2.before_body_text:
                return False
        else:
            if record1.before_title != record1.article.title:
                return False
            if record1.before_body_text != record1.article.body_text:
                return False
        return True
