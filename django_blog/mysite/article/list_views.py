# coding=utf-8
# views视图的名字不一定要取名 views，也可以是其他的取名
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ArticleColumnForm, ArticlePostForm, ArticlePost


def article_titles(request, username=None):
    if username:  # 查看某个作者的所有文章
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo  # UserInfo 数据模型
        except:  # 部分用户没有写用户信息的情况
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()  # 查看所有作者的所有的文章

    paginator = Paginator(articles_title, 10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:  # 请求的页码数值不是整数
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:  # 请求的页码对应的页面为空，或者page为空
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        if userinfo.photo:
            with open(userinfo.getImagePath) as fi:
                base64_img = fi.read()
        else:
            base64_img = ''
        return render(request, "article/list/author_articles.html", {"articles":articles, "page":current_page,
                                                                     "userinfo":userinfo, "user":user, "userimage": base64_img})
    return render(request, 'article/list/article_titles.html', {"articles": articles, "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/list/article_detail.html", {"article": article})


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):  # 文章点赞
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    print(action)
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.user_like.add(request.user)   # 一对多，多对多，都可以用这种方法来进行添加
                return HttpResponse("1")
            else:
                article.user_like.remove(request.user)
                print('-----2------')
                return HttpResponse("2")
        except Exception as e:
            return HttpResponse("no")

