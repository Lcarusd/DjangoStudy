# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse

from rest_framework import filters, generics, permissions, pagination

from school.models import Student, Teacher, Team, Plan, Task, Problem

from school.serializer import (StudentSerializer, TeacherSerializer, TeamSerializer,
                               PlanSerializer, TaskSerializer, ProblemSerializer,)


# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'student': reverse('学生视图', request=request, format=format),
        'teacher': reverse('教师视图', request=request, format=format),
        'team': reverse('团队视图', request=request, format=format),
        'plan': reverse('训练计划视图', request=request, format=format),
        'task': reverse('任务视图', request=request, format=format),
        'problem': reverse('问题视图', request=request, format=format),
    })


class StudentView(generics.ListCreateAPIView):
    '''学生视图'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlanView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class TaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ProblemView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
