# -*- coding: utf-8 -*-
from school.models import Student, Teacher, Team, Plan, Task, Problem
from rest_framework import serializers
import requests


class StudentSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(StudentSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Student
        fields = ('id', 'name', 'team')


class TeacherSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(TeacherSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'team')


class TeamSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(TeamSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Team
        fields = ('id', 'name', 'plan')


class PlanSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(PlanSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Plan
        fields = ('id', 'name', 'task')


class TaskSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(TaskSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = ('id', 'name', 'problem')


class ProblemSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(ProblemSerializer, self).create(data)
        instance.save()
        return instance

    class Meta:
        model = Problem
        fields = ('id', 'name', 'desc')
