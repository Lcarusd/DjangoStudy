# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase

# Create your tests here.


class blogTests(APITestCase):
    '''测试用例'''

    def test_no_login_articles(self):
        url = "/articles/"
        data = {
            "detail": "Authentication credentials were not provided."
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(data, response.data)

    def test_no_login_tags(self):
        url = "/tags/"
        data = {
            "提示": "只允许登录用户访问"
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)
