# -*- coding:utf-8 -*-
__author__ = 'weilijie'
__date__ = '2019-07-30 14:53'

from django.conf.urls import url, include

from organization.views import OrgView, AddUserAskView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask')
]



