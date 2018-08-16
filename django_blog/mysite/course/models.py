# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.db import models
from .fields import OrderField
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User, related_name='courses_user')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(User, related_name="course_joined", blank=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return unicode(self.title)


def user_directory_path(instance, filename):
    return "course/user_{}/{}".format(instance.user.id, filename)  # instance,什么意思


class Lesson(models.Model):
    user = models.ForeignKey(User, related_name='lesson_user')
    course = models.ForeignKey(Course, related_name='lesson')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=user_directory_path)  # 接受上传的视频  ? 参数合适存入
    description = models.TextField(blank=True)
    attach = models.FileField(blank=True, upload_to=user_directory_path)  # 接受上传的附件
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True, for_fileds=['course'])  # 此处的类型是自定义的

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order, unicode(self.title))






