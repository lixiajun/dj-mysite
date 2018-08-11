# coding=utf-8
from django import forms
from .models import Course


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course  # 当模型表中没有 允许为空 的时候，前端有不填的都会被提醒
        fields = ("title", "overview")

