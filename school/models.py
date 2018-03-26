# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Problem(models.Model):
    openstack = models.CharField(u'问题描述', max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Task2(models.Model):
    name = models.CharField(u'任务名称', max_length=255)


class Task1(models.Model):
    desc = models.CharField(u'任务名称', max_length=255)


class Task(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Plan(models.Model):
    name = models.CharField(u'计划名称', max_length=255)
    task = models.ManyToManyField(Task, related_name='Plan')


class Team(models.Model):
    name = models.CharField(u'团队名称', max_length=255)
    plan = models.ManyToManyField(Plan, related_name='Team')


class Student(models.Model):

    name = models.CharField(u'学生姓名', max_length=255)
    team = models.ManyToManyField(Team, related_name='Student')


class Teacher(models.Model):
    name = models.CharField(u'教师姓名', max_length=255)
    team = models.ManyToManyField(Team, related_name='Teacher')
    student = models.ManyToManyField(Student, related_name='Teacher')


class Check(models.Model):
    STATUS_CHOICES = (
        ("1", u'等待'),
        ("2", u'通过'),
        ("3", u'拒绝'),
    )

    name = models.CharField(u'审核名称', max_length=255)
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher)
    status = models.CharField(u'审核状态', max_length=10,
                              choices=STATUS_CHOICES, default=u"等待")

    # Task.objects.filter(Plan__Team__Teacher__pk=1)
    # related_name设置问题
