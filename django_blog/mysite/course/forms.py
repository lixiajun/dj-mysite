# coding=utf-8
from django import forms
from .models import Course,Lesson


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course  # 当模型表中没有 允许为空 的时候，前端有不填的都会被提醒
        fields = ("title", "overview")


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'video', 'description', 'attach']

    def __init__(self, user, *args, **kwargs):  # 重写init函数，每个用户看自己的课程
        super(CreateLessonForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)



