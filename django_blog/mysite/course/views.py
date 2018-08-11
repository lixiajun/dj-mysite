# coding=utf-8
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView  # 基于类的通用视图
from django.views.generic.edit import CreateView, DeleteView
from .models import Course
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
import json

# Create your views here.


class AboutView(TemplateView):
    template_name = "course/about.html"  # 声明模板文件


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "course/course_list.html"


class UserMixin(object):   # mix-in，表明该类会被用于后面的类中，而不是作为视图使用
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):    # 继承的顺序是mix-in类在左边，其他类放在有右边。
    context_object_name = "courses"  # 声明传入模板中的变量的名称
    template_name = 'course/manage/manage_course_list.html'  # 声明模板文件


class CreateCourseView(UserCourseMixin, CreateView):  # CreateView，在是get方法的时候，则显示表单。get方法不用自己写
    fields = ['title', 'overview']  # 声明在表单中显示的字段
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)  # form也会在静态获取页面的时候被渲染
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form": form})


class DeleteCourseView(UserCourseMixin, DeleteView):  # DeleteView已经执行了删除动作，后续代码就不需要重复删除动作

    #template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp



