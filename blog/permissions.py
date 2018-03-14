# -*- coding: utf-8 -*-
from rest_framework import permissions


# class IsArticleOwner(permissions.BasePermission):

#     message = u'非文章所有者'

#     def has_object_permission(self, request, view, obj):
#         # obj为Article对象
#         return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = '需登录才能继续操作'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
