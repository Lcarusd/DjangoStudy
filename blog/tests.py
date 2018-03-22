# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase

from blog.models import Article, Record

from django.contrib.auth.models import User

from collections import OrderedDict

# Create your tests here.


class blogTests(APITestCase):
    '''测试用例'''

    def setUp(self):
        self.user = dict(username='admin', email='', password='admin123')
        User.objects.create_superuser(**self.user)
        self.client.login(**self.user)

    # 测试用户登录...

    def test_login(self):
        '''测试已登录状态用户登录'''
        self.user = dict(username='abc', email='', password='admin123')
        User.objects.create_user(**self.user)

        url = "/login/"
        data = {
            "username": "abc",
            "password": "admin123",
        }
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_failed_login(self):
        '''测试登录失败'''
        url = "/login/"
        data = {
            "username": "xyz",
            "password": "admin123",
        }
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    # 测试用户登出...

    def test_logout(self):
        '''测试已登录用户登出'''
        url = "/logout/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    # 测试查看用户列表...

    def test_admin_users(self):
        '''管理员登录状态查看并新增用户'''
        url = "/users/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)   # 无返回文本内容

        url = "/users/"
        data = {
            "username": "admins",
            "password": "admin123",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
        del response.data['password']
        message = {
            'id': 2,
            'username': 'admins',
        }
        self.assertDictEqual(response.data, message)

    # 测试查看并新建文章...

    def test_articles(self):
        '''已登录状态新建并查看文章'''
        # 新建文章
        url = "/articles/"
        data = {
            "title": "测试用例文章",
            "body_text": "测试用例文章测试用例文章",
        }
        response = self.client.post(url, data=data, format="json")

        # 查看文章
        url = "/articles/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        article = Article.objects.get(pk=1)
        message = '测试用例文章'
        self.assertEqual(article.title, message)

    # 测试文章详情页查看更新...

    def test_article(self):
        '''测试已登录状态查看或更新文章详情页'''
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "fdsafadsfadsf"
        }
        response = self.client.post(path=url, data=data, format="json")

        url = "/article/1/"
        data = {
            "title": "body_title",
            "body_text": "fdsafadsfadsf",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        message = {
            'id': 1,
            'title': 'body_title',
            'body_text': 'fdsafadsfadsf',
            'status': 'PUBLIC'
        }
        del response.data['users']
        self.assertDictEqual(response.data, message)

    # 测试文章点赞...

    def test_article_like(self):
        '''测试已登录状态点赞文章'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "机器学习",
            "body_text": "机器学习(Machine Learning, ML)是一门多领域交叉学科。第一次修改。第二次修改。",
            "post_status": "post"
        }
        response = self.client.post(path=url, data=data, format='json')

        # 文章是否被点赞
        url = "/likes/"
        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 0)

        # 点赞文章
        data = {
            "article": article.id
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        message = {
            'article': 1
        }
        self.assertDictEqual(response.data, message)

        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 1)

        # 再次点赞不影响文章的like_count
        response = self.client.post(path=url, data=data, format='json')
        article = Article.objects.filter(title="机器学习").first()
        self.assertEqual(article.like_count, 1)

    def test_no_article_like(self):
        '''测试登录用户点赞文章（文章未找到）'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "机器学习",
            "body_text": "机器学习(Machine Learning, ML)是一门多领域交叉学科。第一次修改。第二次修改。",
            "status": "HIDE"
        }
        response = self.client.post(path=url, data=data, format='json')

        # 非文章作者登录
        self.user = dict(username='abc', email='', password='admin123')
        User.objects.create_user(**self.user)
        url = "/login/"
        data = {
            "username": "abc",
            "password": "admin123",
        }
        response = self.client.post(path=url, data=data, format="json")

        url = "/likes/"
        article = Article.objects.filter(title="机器学习").first()
        data = {
            "article": article.id
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    # 测试查看文章编辑记录...

    def test_records(self):
        '''测试已登录状态查看文章编辑记录'''
        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "fdsafadsfadsf"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成一条record
        url = "/article/1/"
        data = {
            "title": "body_title_1",
            "body_text": "fdsafadsfadsfqq",
        }
        response = self.client.put(url, data, format="json")

        # 查看record记录
        url = "/records/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        record = Record.objects.filter(pk=1).first()
        self.assertIsNotNone(record)

    # 测试标签查看功能...

    def test_tags(self):
        '''测试已登录状态查看标签'''
        # 创建文章
        url = "/articles/"
        data = {
            "title": "机器学习",
            "body_text": "机器学习(Machine Learning, ML)是一门多领域交叉学科。第一次修改。第二次修改。",
        }
        response = self.client.post(path=url, data=data, format='json')

        # 生成一条record
        url = "/article/1/"
        data = {
            "title": "机器学习",
            "body_text": "机器学习是一门多领域交叉学科。第一次修改。第二次修改。",
        }
        response = self.client.put(url, data, format="json")

        url = "/tags/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        message = OrderedDict([
            ('results',
             [OrderedDict([('id', 1), ('name', '修改'), ('count', 1)]),
              OrderedDict([('id', 2), ('name', '交叉学科'), ('count', 1)]),
              OrderedDict([('id', 3), ('name', '一门'), ('count', 1)])])
        ])
        del response.data['count']
        del response.data['next']
        del response.data['previous']
        self.assertAlmostEqual(response.data, message)

    # 测试对比文章编辑记录...

    def test_before_title_diff(self):
        '''测试before_title接口对比(已设置record2)'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "titletitle"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成第一条record
        url = "/article/1/"
        data = {
            "title": "body_title_1",
            "body_text": "titletitle",
        }
        response = self.client.put(url, data, format="json")

        # 生成第二条record
        url = "/article/1/"
        data = {
            "title": "body_title_2",
            "body_text": "titletitle",
        }
        response = self.client.put(url, data, format="json")

        # 接口对比
        url = "/diff/"
        data = {
            "record1": 2,
            "record2": 3
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, False)

    def test_before_title_diff(self):
        '''测试before_body_text接口对比(已设置record2)'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "text"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成第一条record
        url = "/article/1/"
        data = {
            "title": "title",
            "body_text": "texttext",
        }
        response = self.client.put(url, data, format="json")

        # 生成第二条record
        url = "/article/1/"
        data = {
            "title": "title",
            "body_text": "texttexttext",
        }
        response = self.client.put(url, data, format="json")

        # 接口对比
        url = "/diff/"
        data = {
            "record1": 2,
            "record2": 3
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, False)

    def test_before_title_diff(self):
        '''测试before_title接口对比(未设置record2)'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "titletitle"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成一条record
        url = "/article/1/"
        data = {
            "title": "title_1",
            "body_text": "titletitle",
        }
        response = self.client.put(url, data, format="json")

        # 接口对比
        article = Article.objects.get(pk=1)
        url = "/diff/"
        data = {
            "record1": 1,
            "article": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, False)

    def test_before_title_diff(self):
        '''测试before_body_text接口对比(未设置record2)'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "text"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成一条record
        url = "/article/1/"
        data = {
            "title": "title",
            "body_text": "texttext",
        }
        response = self.client.put(url, data, format="json")

        # 接口对比
        # article = Article.objects.get(pk=1)
        url = "/diff/"
        data = {
            "record1": 1,
            "record2": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, False)
        # print(response.data)

    def test_Diff(self):
        '''测试返回True状态对比文章编辑记录'''
        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "text"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 生成第一条record
        url = "/article/1/"
        data = {
            "title": "title",
            "body_text": "text"
        }
        response = self.client.put(url, data, format="json")

        # 生成第二条record
        url = "/article/1/"
        data = {
            "title": "title",
            "body_text": "text"
        }
        response = self.client.put(url, data, format="json")

        # 已设置record2接口对比
        url = "/diff/"
        data = {
            "record1": 1,
            "record2": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, True)

        # 未设置record2接口对比
        url = "/diff/"
        data = {
            "record1": 1,
            "record2": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.data, True)

    # 测试信号发送与接收....

    def test_signal(self):
        '''测试登录状态信号发送与接收'''

        # 创建文章
        url = "/articles/"
        data = {
            "title": "title",
            "body_text": "fdsafadsfadsf"
        }
        response = self.client.post(path=url, data=data, format="json")

        # 判断记录是否存在
        record = Record.objects.filter(pk=2).first()
        self.assertIsNone(record)

        # 更新文章
        url = "/article/1/"
        data = {
            "title": "body_title_1",
            "body_text": "fdsafadsfadsfqq",
        }
        response = self.client.put(url, data, format="json")

        message = {
            'id': 1,
            'title': 'body_title_1',
            'body_text': 'fdsafadsfadsfqq',
            'status': 'PUBLIC'
        }
        del response.data['users']
        self.assertDictEqual(response.data, message)

        # 判断记录是否存在
        record = Record.objects.filter(pk=2).first()
        self.assertIsNotNone(record)
