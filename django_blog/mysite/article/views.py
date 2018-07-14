# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST  # 只接受post的方式提交的数据
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ArticleColumn, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticlePost, ArticleTagForm


# Create your views here.


@login_required(login_url='/account/login/')
@csrf_exempt  # 解决表单中的csrf问题
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, 'column_form': column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)  # 两个条件，并
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form,
                                                                    "article_columns": article_columns})


@login_required(login_url='/account/login')
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles, 10)
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
    return render(request, 'article/column/article_list.html', {"articles": articles, "page": current_page})


@login_required(login_url='/account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST["article_id"]
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request, article_id):  # article_id 接收文章的id
    if request.method == "GET":
        context = dict()
        context['article_columns'] = request.user.article_column.all()
        context['article'] = article = ArticlePost.objects.get(id=article_id)
        context['this_article_form'] = ArticlePostForm(initial={"title": article.title})
        context['this_article_column'] = article.column
        return render(request, "article/column/redit_article.html", context)
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except Exception as e:
            return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article__tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags": article_tags,
                                                             "article_tag_form": article__tag_form})
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)  # 创建一个对象，没有保存
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cant be saved")
        else:
            return HttpResponse("sorry,the form is not valid")


@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_article_tag(request):
    print request.POST.items()
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")







