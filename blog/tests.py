# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase

from blog.models import Article

from django.contrib.auth.models import User

# Create your tests here.


class blogTests(APITestCase):
    '''测试用例'''

    def setUp(self):
        pass

    # 测试用户登录...

    def test_nologin_login(self):
        '''测试已登录状态用户登录'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/login/"
        data = {
            "username": "admin",
            "password": "admin123",
        }
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, 200)

    # def test_login(self):
    #     '''测试未登录状态登录'''
    #     url = "/login/"
    #     response = self.client.get(url, fromat="json")
    #     self.assertEqual(response.status_code, 405)

    # 测试用户登出...

    def test_logout(self):
        '''测试已登录用户登出'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/logout/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

    def test_nologin_logout(self):
        '''测试未登录用户登出'''
        url = "/logout/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 403)

    # 测试查看用户列表...

    def test_admin_users(self):
        '''管理员登录状态查看并新增用户'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/users/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        url = "/users/"
        data = {
            "username": "admins",
            "password": "admin123",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_users(self):
        '''非管理员用户登录状态查看用户列表'''
        url = "/logout/"
        data = {
            "username": "admin",
            "password": "admin123",
        }
        response = self.client.get(url, data=data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_nologin_users(self):
        '''未登录状态查看用户列表'''
        url = "/logout/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 403)

    # 测试查看并新建文章...

    def test_nologin_articles(self):
        '''未登录状态查看并新建文章'''
        url = "/articles/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_articles(self):
        '''已登录状态查看并新建文章'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/articles/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        url = "/articles/"
        data = {
            "title": "测试用例文章",
            "body_text": "测试用例文章测试用例文章",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)

    # 测试文章详情页查看...

    def test_nologin_article(self):
        '''测试未登录状态查看或更新文章详情页'''
        pass

    def test_article(self):
        '''测试已登录状态查看文章详情页'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "fdsafadsfadsf"
        }
        response = self.client.post(path=url, data=data, format="json")

        url = "/article/1/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

    # 测试文章点赞...

    def test_article_like(self):
        '''测试已登录状态点赞文章'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        data = {
            "title": "机器学习",
            "body_text": "机器学习(Machine Learning, ML)是一门多领域交叉学科。第一次修改。第二次修改。",
            "post_status": "post"
        }
        url = "/articles/"
        response = self.client.post(path=url, data=data, format='json')

        url = "/likes/"
        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 0)

        data = {
            "article": article.id
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 1)

        # 再次点赞不影响文章的like_count
        response = self.client.post(path=url, data=data, format='json')
        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 1)

    def test_nologin_article_like(self):
        '''测试未登录状态点赞文章'''
        url = "/likes/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 403)

    # 测试查看文章编辑记录...

    def test_nologin_records(self):
        '''测试未登录状态查看文章编辑记录'''
        url = "/records/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 403)

    def test_records(self):
        '''测试已登录状态查看文章编辑记录'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/records/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

    # 测试标签查看功能...

    def test_nologin_tags(self):
        '''测试未登录状态查看标签'''
        url = "/tags/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_tags(self):
        '''测试已登录状态查看标签'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/tags/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

    # 测试对比文章编辑记录...

    def test_nologin_Diff(self):
        '''测试未登录状态对比文章编辑记录'''
        url = "/diff/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_Diff(self):
        '''测试已登录状态对比文章编辑记录'''
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

        url = "/diff/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 405)
