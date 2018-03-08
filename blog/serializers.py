# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import serializers

from blog.models import Article, Like


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
    like_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_like_users(self, obj):
        # obj  为一个文章实例
        data = list(Like.objects.filter(article=obj).order_by(
            '-id').values_list('user__username', flat=True))
        return data

    def get_users(self, obj):
        # 获取文章作者名称
        return obj.users.all().values_list(
            'username', flat=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'users', 'like_count', 'like_users')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'body_text', 'status')


class LikeSerializer(serializers.ModelSerializer):
    # 只有公开的文章可以点赞
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
