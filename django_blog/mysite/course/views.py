# coding=utf-8
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView  # 基于类的通用视图
from django.views.generic.edit import CreateView, DeleteView
from .models import Course, Lesson
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm, CreateLessonForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
import json
from django.views import View  # 所有基于类的视图的 基类
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin # 提供模板渲染的机制，子类中可以指定模板文件和渲染数据
# Create your views here.


import sys

default_encoding = 'utf-8'   # 设置python的系统编码为utf-8 ，解决模板渲染的对象有中文的问题。 这里是 CreateLessonView的form.course有中文
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


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
            new_course.title = unicode(new_course.title)
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


class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login"

    # 自己写 get 和 post方法
    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'  # 继承的TemplateResponseMixin,所以此处直接指定模板文件

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course': course})


class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self.render_to_response({"lesson": lesson})


class StudentListLessonView(ListLessonsView):  # 学生能够看到内容标题和详细内容
    template_name = "course/slist_lessons.html"  # 重写模板文件即可

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")

