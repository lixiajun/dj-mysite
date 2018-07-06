# coding=utf-8
# views视图的名字不一定要取名 views，也可以是其他的取名
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ArticleColumnForm, ArticlePostForm, ArticlePost, CommentForm
import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
    total_views = r.incr("article:{}:views".format(article.id))  # 自增长
    r.zincrby('article_ranking', article.id, 1)  # 访问一次，那么 article_ranking 就记录该文章id的值增加1

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)   # 取所有文章的前10个
    article_ranking_ids = [int(id) for id in article_ranking]  # 前10的id的列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))  # 前10的文章对象
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))  # 按照访问次数对文章进行排名

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article  # 这是因为表单里面没有保存文章的信息，所以这里额外保存
            new_comment.commentator = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views,
                                                                "most_viewed": most_viewed, "comment_form": comment_form})



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

