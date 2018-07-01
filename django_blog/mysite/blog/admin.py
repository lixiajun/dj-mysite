#coding=utf-8
from django.contrib import admin
from .models import BlogArticles

class BlogArticlesAdmin(admin.ModelAdmin):  #自定义一些排列需求
    list_display = ('title', 'author', 'publish')  #哪些字段显示
    list_filter = ('publish', 'author') #按照什么来排序
    search_fields = ('title', 'body')  #从哪里搜索
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish', 'author']

admin.site.register(BlogArticles,BlogArticlesAdmin)  #可以通过管理后台来管理表，增加记录

# Register your models here.
