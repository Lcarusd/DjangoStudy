# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 09:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('body_text', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('like_count', models.IntegerField(default=0, verbose_name='\u6587\u7ae0\u88ab\u70b9\u8d5e\u7684\u6b21\u6570')),
                ('status', models.CharField(choices=[('PUBLIC', '\u516c\u5f00\u6587\u7ae0'), ('HIDE', '\u9690\u85cf\u6587\u7ae0')], default='PUBLIC', max_length=10, verbose_name='\u6587\u7ae0\u72b6\u6001')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
