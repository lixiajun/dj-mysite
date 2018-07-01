#coding=utf-8

from django.contrib import admin
from .models import UserProfile, UserInfo

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ('phone',)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "company", "profession", "address", "aboutme","photo")
    list_filter = ("school", "company", "profession")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)

#admin.py的作用是让  django自带的后台 能够管理  一些内容