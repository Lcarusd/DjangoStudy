# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-14 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180314_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='count',
            field=models.IntegerField(verbose_name='\u6807\u7b7e\u4f7f\u7528\u9891\u6b21'),
        ),
    ]
