# -*- coding: utf-8 -*-
from school.models import Student, Teacher, Team, Plan, Task, Problem
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(StudentSerializer, self).create(data)
        # team = Team.objects.filter(name="seclover").first()
        # instance.team = team
        instance.save()
        return instance

    class Meta:
        model = Student
        fields = ('id', 'name', 'team')


class TeacherSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(TeacherSerializer, self).create(data)
        # 若采用create方法创建对象，会将create和save同时进行
        # team = Team.objects.create(name="seclover")
        # team = Team.objects.filter(name="seclover").first()
        # instance.team.add(team)
        instance.save()
        return instance

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'team')


class TeamSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(TeamSerializer, self).create(data)
        # plan = Plan.objects.filter(name="CodingPlan").first()
        # instance.plan.add(plan)
        instance.save()
        return instance

    class Meta:
        model = Team
        fields = ('id', 'name', 'plan')


class PlanSerializer(serializers.ModelSerializer):

    def create(self, data):
        instance = super(PlanSerializer, self).create(data)
        # task = Task.objects.filter(name="Djnagogogo").get()
        # instance.task.add(task)
        instance.save()
        return instance

    class Meta:
        model = Plan
        fields = ('id', 'name', 'task')


class TaskSerializer(serializers.ModelSerializer):
    # problem = serializers.SerializerMethodField()

    # def get_problem(self, obj):
    #     return obj.problem.all().values_list(
    #         'problem', flat=True)

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
