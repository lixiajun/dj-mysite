# coding=utf-8
from django.conf.urls import url
from .views import (AboutView,
                    CourseListView,
                    ManageCourseListView,
                    CreateCourseView,
                    DeleteCourseView,
                    CreateLessonView,
                    ListLessonsView,
                    DetailLessonView,
                    StudentListLessonView)
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^course-list/$', CourseListView.as_view(), name="course_list"),  # 所有的课程
    url(r'^manage-course/$', ManageCourseListView.as_view(), name="manage_course"),  # 管理课程
    url(r'^create-course/$', CreateCourseView.as_view(), name="create_course"),
    url(r'^delete-course/(?P<pk>\d+)/$', DeleteCourseView.as_view(), name="delete_course"),
    url(r'^create-lesson/$', CreateLessonView.as_view(), name="create_lesson"),
    url(r'^list-lessons/(?P<course_id>\d+)/$', ListLessonsView.as_view(), name='list_lessons'),
    url(r'^detail-lesson/(?P<lesson_id>\d+)/$', DetailLessonView.as_view(), name='detail_lesson'),
    url(r'^lessons-list/(?P<course_id>\d+)/$', StudentListLessonView.as_view(), name='lessons_list'),
]