# -*- coding: utf-8 -*-
from django.conf.urls import url

from blog.views import (ArticleListView, ArticleView, UserDetail, UserLikeView,
                        UserListView, UserLoginView, UserLogoutView, api_root)

urlpatterns = [
    url(r'^$', api_root),
    url(r'^login/$', UserLoginView.as_view(), name=u'登录'),
    url(r'^logout/$', UserLogoutView.as_view(), name=u'登出'),
    url(r'^users/$', UserListView.as_view(), name=u'用户列表和创建'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(), name=u'用户详情表'),
    url(r'^articles/$', ArticleListView.as_view(), name=u'文件列表和创建'),
    url(r'^article/(?P<pk>[0-9]+)/$',
        ArticleView.as_view(),
        name=u'文章的查|删|改'),
    url(r'^likes/$', UserLikeView.as_view(), name=u'点赞创建'),
]

# urlpatterns = [
#   url(正则表达式, view函数，参数，别名)
# ]
