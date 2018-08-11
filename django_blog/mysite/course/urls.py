# coding=utf-8
from django.conf.urls import url
from .views import AboutView, CourseListView, ManageCourseListView, CreateCourseView, DeleteCourseView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^course-list/$', CourseListView.as_view(), name="course_list"),  # 所有的课程
    url(r'^manage-course/$', ManageCourseListView.as_view(), name="manage_course"),  # 管理课程
    url(r'^create-course/$', CreateCourseView.as_view(), name="create_course"),
    url(r'^delete-course/(?P<pk>\d+)/$', DeleteCourseView.as_view(), name="delete_course"),
]