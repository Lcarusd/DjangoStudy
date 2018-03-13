# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 11:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='article', to='blog.Tags', verbose_name='\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='record',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='\u7f16\u8f91\u6587\u7ae0'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7f16\u8f91\u4eba'),
        ),
    ]
