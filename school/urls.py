# -*- coding: utf-8 -*-
from django.conf.urls import url

from school.views import (StudentView, TeacherView, TeamView,
                          PlanView, TaskView, ProblemView, api_root)


urlpatterns = [
    url(r'^$', api_root),
    url(r'^student/$', StudentView.as_view(), name=u'学生视图'),
    url(r'^teacher/$', TeacherView.as_view(), name=u'教师视图'),
    url(r'^team/$', TeamView.as_view(), name=u'团队视图'),
    url(r'^plan/$', PlanView.as_view(), name=u'训练计划视图'),
    url(r'^task/$', TaskView.as_view(), name=u'任务视图'),
    url(r'^problem/$', ProblemView.as_view(), name=u'问题视图'),
]
