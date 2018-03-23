# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Problem(models.Model):
    openstack = models.CharField(u'问题描述', max_length=255)

    tasks = GenericRelation(Task)


class Problem1(models.Model):
    name = models.CharField(u'问题名称', max_length=255)
    desc = models.CharField(u'问题描述', max_length=255)

    tasks = GenericRelation(Task)


class Task(models.Model):
    desc = models.CharField(u'任务名称', max_length=255)
    problem = models.ManyToManyField(Problem, related_name='Task')

    plans = GenericRelation(Plan)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Task1(models.Model):
    name = models.CharField(u'任务名称', max_length=255)
    problem = models.ManyToManyField(Problem, related_name='Task')

    plans = GenericRelation(Plan)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Task2(models.Model):
    name = models.CharField(u'任务名称', max_length=255)
    problem = models.ManyToManyField(Problem, related_name='Task')

    plans = GenericRelation(Plan)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Plan(models.Model):
    name = models.CharField(u'计划名称', max_length=255)
    task = models.ManyToManyField(Task, related_name='Plan')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# content = ContentType.objects.filter(app_label='school', model='plan').first()
# response = models.OftenAskedQuestion.objects.filter(content_type=content, object_id=obj.pk).all()


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
        (WAIT, u'等待'),
        (ACCEPT, u'通过'),
        (REFUSE, u'拒绝'),
    )

    name = models.CharField(u'审核名称', max_length=255)
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher)
    status = models.CharField(u'审核状态', max_length=10,
                              choices=STATUS_CHOICES, default=WAIT)

    # Task.objects.filter(Plan__Team__Teacher__pk=1)
    # related_name设置问题
