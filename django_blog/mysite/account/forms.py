#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):  # 表单类,不对数据库有操作
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # widget 规定标签类型，type


class RegistrationForm(forms.ModelForm):  # 将表单中的数据写入数据库表或者跟新数据的话，要继承ModelForm
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)
    # 从数据库的表的字段映射成form表单，其中 password和password2两个属性重新定义。意味着覆盖或者不需要在
    # 内部类Meta中声明的字段

    class Meta:
        model = User   # 对应数据库中的表的名字
        fields = ("username", "email")  # 选择需要操作的字段
            # 此处就没有声明password，因为上面已经声明了

    def clean_password2(self):   # 作用是检验用户输入的两个密码是否一致。在调用 is_valid()的方法的时候会执行。
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)




