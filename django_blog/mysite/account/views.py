#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login  #默认的用户认证和管理应用
from .forms import LoginForm, RegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserProfileForm, UserInfoForm, UserForm
from mysite.settings import UPLOAD_IMAGE_DIR
import os
from django.core.urlresolvers import reverse
# Create your views here.


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)  #传入表单的数据，绑定一个实例
        if login_form.is_valid():
            cd = login_form.cleaned_data  #字典类型数据
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("wellcome you.you have been authenticated successfully")
            else:
                return HttpResponse("failed ")
        else:
            return HttpResponse("invalid login")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False) # save方法可以将数据保存到对应的数据库中，这里是false，就是没有保存，而是生成了一个对象
            new_user.set_password(user_form.cleaned_data['password'])  #设置密码
            new_user.save() #保存到数据库
            new_profile = userprofile_form.save(commit=False)  #新建一个对象
            new_profile.user = new_user
            new_profile.save()
            print(new_profile.user_id)
            UserInfo.objects.create(user=new_user) # 新建用户的同时，在UserInfo表里面也新建数据
            return HttpResponseRedirect(reverse('account:user_login'))
        else:
            return HttpResponse("sorry, you can not registe")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


@login_required(login_url='/account/login/')  # 装饰器，查看是否已经登录，将没有登录的转到登录页面
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    user_photo_url = userinfo.getImagesUrl
    with open(userinfo.getImagePath) as fi:
        image = fi.read()
    return render(request,"account/myself.html",{'user':user, 'userprofile':userprofile, 'userinfo':userinfo, "userimage":image})


@login_required(login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":  #是post，则更新数据
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():  # * 是 and的意思， + or的意思
            user_cd = user_form.cleaned_data  #字典类型，：“净化后的数据”
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')  #页面的跳转，是绝对路径
    else:
        user_form = UserForm(instance=request.user)  # 将用户已有的信息显示
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth,   # 将用户已有的信息显示
                                                    "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                                 "company": userinfo.company,
                                                 "profession": userinfo.profession,
                                                 "address": userinfo.address,
                                                 "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html",
                      {"user_form": user_form,
                       "userprofile_form": userprofile_form,
                       "userinfo_form": userinfo_form})


@login_required(login_url='/account/login')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']   # img 是对图片进行base64编码的内容
        img_name = str(request.user.id) + '.jpg'
        user_iamge_path = os.path.join(UPLOAD_IMAGE_DIR, str(request.user.id) + '.jpg')
        with open(user_iamge_path, 'w+') as fi:
            fi.write(img)
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img_name  # 存储图片的名字
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html')


