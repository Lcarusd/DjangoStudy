# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.


class AppTests(APITestCase):
    '''测试用例'''

    def test_no_login_articles(self):
        url = "/articles/"
        data = {
            "detail": "Authentication credentials were not provided."
        }
        response = self.client.get(url, format='json')
        self.assertDictEqual(data, response.data)
