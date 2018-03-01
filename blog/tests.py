# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.


class AppTests(APITestCase):
    '''
    测试
    def test_xxx(self):
        url = "/xxx/xxxxx/"
        data={}
        response = self.client.get(url, format='json')
        self.assertDictEqual(data, response.data)
    '''
    # fixtures = ['mytest.json']

    # def setUp(self):
    #     data = {
    #         "username": 'admin',
    #         "password": 'password123',
    #     }
    #     self.client.post('/login/', data)

    def test_no_login_articles(self):
        url = "/articles/"
        data = {
            "detail": "Authentication credentials were not provided."
        }
        response = self.client.get(url, format='json')
        self.assertDictEqual(data, response.data)
    # def test_login_articles(self):
    #     url = "/articles/"
    #     data = [
    #         {
    #             "id": 1,
    #             "title": "标题admin公开",
    #             "user": [
    #                 "admin"
    #             ],
    #             "like_count": 0,
    #             "like_users": []
    #         },
    #         {
    #             "id": 2,
    #             "title": "标题admin隐藏",
    #             "user": [
    #                 "admin"
    #             ],
    #             "like_count": 0,
    #             "like_users": []
    #         }
    #     ]
    #     response = self.client.get(url, format='json')
    #     self.assertListEqual(data, response.data)
