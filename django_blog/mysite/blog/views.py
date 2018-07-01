#coding=utf-8
from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
# Create your views here.


def blog_title(request):  #基于函数的视图，视图函数
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs": blogs})


def blog_article(request, article_id):
    #article = BlogArticles.objects.get(id=article_id)
    article = get_object_or_404(BlogArticles, id=article_id) #第一个参数是models类，第二个参数是查询类型
    pub = article.publish
    return render(request, "blog/content.html", {"article": article, "publish": pub})


