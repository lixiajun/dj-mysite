#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mysite.settings import UPLOAD_IMAGE_DIR, IMAGE_URL, DEFAULT_PERSON_IMAGE_PATH
import os


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)  # 一对一的关系
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)  # blank表明字段可以为空
    photo = models.CharField(max_length=100, blank=True)   # 上传图片的名字 ，不用图片的路径是为了让存储图片的目录具有灵活性

    def __str__(self):
        return "user:{}".format(self.user.username)

    @property  # 将方法变成属性调用
    def getImagesUrl(self):
        return os.path.join(IMAGE_URL, self.photo)

    @property
    def getImagePath(self):
        if self.photo:
            return os.path.join(UPLOAD_IMAGE_DIR, self.photo)

