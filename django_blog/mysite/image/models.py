# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from slugify import slugify

# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User, related_name="images")
    title = models.CharField(max_length=300)
    url = models.URLField()
    slug = models.SlugField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)  # auto_now_add 是实例创建的时候，会自动保存时间；db_index 是将此字段作为索引
    image = models.ImageField(upload_to='images/%s/%m/%d')  # ImageField继承FileField，能够接受上传的文件，upload_to规定了上传的路径

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)


