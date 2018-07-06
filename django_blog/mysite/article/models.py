# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone   # settings中的TIME_ZONE要改为'Asia/Shanghai'
from django.core.urlresolvers import reverse
from slugify import slugify
# Create your models here.


class ArticleColumn(models.Model):  # 文章的栏目，跟用户绑定
    user = models.ForeignKey(User, related_name='article_column')  # 一对多的关系,建立外键关系。使用方法是 user.article_column
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):  # 文章的内容
    author = models.ForeignKey(User, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)  # 让url更易读
    column = models.ForeignKey(ArticleColumn, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(User, related_name="articles_like", blank=True)

    class Meta:
        ordering = ("-updated",)  # 按照文章的标题来排序，作用在查询出相关的文章之后的排序
        index_together = (('id', 'slug'),)  # 数据库中建立索引。通过文章的id和slug获取文章对象

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)  # 重写save函数，增加一个存储内容
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):  # 在模型里写方法，而不是在其他地方。目的是获取到该对象（记录）的时候就能使用这个方法。模板可以直接用。
        return reverse("article:article_detail", args=[self.id, self.slug])  # 生成文章对象的url，以id和文章名来作为url。既确保美观，又确保唯一性

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])  # 给不需要登录的用户使用的


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comments")
    commentator = models.ForeignKey(User, related_name="commentator")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)

