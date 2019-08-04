# _*_ coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
# from django.http import HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from organization.forms import UserAskForm

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        host_orgs = all_orgs.order_by("-click_nums")[:3]
        all_city = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            #虽然在courseorg中定义了外键city，但是在数据库中存储是city_id
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #做类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort','')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")


        org_nums = all_orgs.count()
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_city,
            "org_nums": org_nums,
            'citys_id': city_id,
            'category': category,
            'hot_orgs': host_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json,charset=utf-8')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json,charset=utf-8')


