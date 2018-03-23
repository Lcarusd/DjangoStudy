# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Problem(models.Model):
    name = models.CharField(u'问题名称', max_length=255)
    desc = models.CharField(u'问题描述', max_length=255)


class Task(models.Model):
    name = models.CharField(u'任务名称', max_length=255)
    problem = models.ManyToManyField(Problem, related_name='Task')


class Plan(models.Model):
    name = models.CharField(u'计划名称', max_length=255)
    task = models.ManyToManyField(Task, related_name='Plan')


class Team(models.Model):
    name = models.CharField(u'团队名称', max_length=255)
    plan = models.ManyToManyField(Plan, related_name='Team')


class Student(models.Model):
    name = models.CharField(u'学生姓名', max_length=255)
    team = models.ForeignKey(Team, related_name='Student')


class Teacher(models.Model):
    name = models.CharField(u'教师姓名', max_length=255)
    team = models.ManyToManyField(Team, related_name='Teacher')
    # Task.objects.filter(Plan__Team__Teacher__pk=1)
    # related_name设置问题
