# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, pagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from blog.models import Article, Tags, Record
# from blog.permissions import
from blog.serializers import (ArticleListSerializer, ArticleSerializer,
                              LikeSerializer, UserLoginSerializer, UserSerializer,
                              RecordListSerializer, TagListSerializer, TagSerializer,)

# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('登录', request=request, format=format),
        'logout': reverse('登出', request=request, format=format),
        'users': reverse('用户列表和创建', request=request, format=format),
        'articles': reverse('文件列表和创建', request=request, format=format),
        'likes': reverse('点赞创建', request=request, format=format),
        'records': reverse('记录列表', request=request, format=format),
        'tags': reverse('标签创建', request=request, format=format),
    })


class CommonPagination(pagination.PageNumberPagination):
    '''分页器'''
    max_page_size = 500
    page_size_query_param = 'size'
    page_size = 10


class UserLoginView(generics.GenericAPIView):
    '''登录'''
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 返回空，因为rest通过状态码判断
        return Response()


class UserLogoutView(generics.GenericAPIView):
    '''登出'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            request.session.flush()
        except KeyError:
            pass
        return Response()


class UserListView(generics.ListCreateAPIView):
    '''
    user列表视图
    继承ListCreateAPIView,包含创建、列表
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 仅限管理员可使用此视图
    permission_classes = (permissions.IsAdminUser, )


class UserDetail(generics.RetrieveAPIView):
    '''
    user详情页视图
    GET:返回一个现有用户实例
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserLikeView(generics.CreateAPIView):
    '''
    用户点赞视图
    '''

    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ArticleListView(generics.ListCreateAPIView):
    '''文章列表视图'''
    queryset = Article.objects.all().order_by('-like_count')
    # 对文章状态与用户进行筛选
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('status', 'users')
    search_fields = ('title', 'user__username')
    # IsAuthenticated 登陆用户可使用此视图
    permission_classes = (permissions.IsAuthenticated, )
    # 分页
    pagination_class = CommonPagination

    # 校验用户，确定所需展示的文章
    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return Article.objects.filter(Q(status='PUBLIC') | Q(users__in=[user]))
        else:
            return Article.objects.filter(status='PUBLIC')

    # 建立序列化，创建或显示列表
    def get_serializer_class(self):
        if self.request.method == 'POST':
            # 创建
            self.serializer_class = ArticleSerializer
        else:
            # 显示
            self.serializer_class = ArticleListSerializer
        return super(ArticleListView, self).get_serializer_class()

    def perform_create(self, serializer):
        # 创建前传入user
        serializer.save()


class ArticleView(generics.RetrieveUpdateDestroyAPIView):
    '''文章详情页视图'''
    article_queryset = Article.objects.all()
    record_queryset = Record.objects.all()

    # 复用了文章列表中的序列化
    serializer_class = ArticleSerializer
    # serializer_class = ArticleDetailSerializer
    # 增加了文章所有者的权限判断
    permission_classes = (permissions.IsAuthenticated,)

    # 筛选基于当前用户的查询集，并做权限验证
    def get_queryset(self):
        users = self.request.user
        if users and users.is_authenticated:
            return Article.objects.filter(Q(status='PUBLIC') | Q(users=users))
        else:
            return Article.objects.filter(status='PUBLIC')

    def perform_create(self, serializer):
        # 创建前传入user
        serializer.save(user=self.request.user)


class RecordListView(generics.ListAPIView):
    '''
    记录列表接口 用于展示修改记录与筛选字段(编辑人、编辑文章)
    '''
    queryset = Record.objects.all()
    # 筛选器，增加记录回退功能及对编辑人、编辑文章进行筛选
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'article', 'update_datetime',)

    # 展示修改记录
    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.serializer_class = RecordListSerializer
        return super(RecordListView, self).get_serializer_class()


class TagListView(generics.ListCreateAPIView):
    '''tag列表接口 用于展示标签信息及使用频次'''
    queryset = Tags.objects.all()

    # 展示tag信息
    def get_serializer_class(self):
        if self.request.method == 'POST':
            # 创建tag
            self.serializer_class = TagSerializer
        else:
            # 展示tag
            self.serializer_class = TagListSerializer
        return super(TagListView, self).get_serializer_class()
