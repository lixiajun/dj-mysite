# coding=utf-8
# views视图的名字不一定要取名 views，也可以是其他的取名
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from .forms import ArticleColumnForm, ArticlePostForm, ArticlePost


def article_titles(request):
    articles_title = ArticlePost.objects.all()
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
    return render(request, 'article/list/article_titles.html', {"articles": articles, "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/list/article_detail.html", {"article": article})
