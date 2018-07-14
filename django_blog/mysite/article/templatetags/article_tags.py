# coding=utf-8
from django import template      # 跟模板有关的类和方法

register = template.Library()       #变量名称就是register
from article.models import ArticlePost
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
# 这个文件的作用是可以在 模板中引用这里的方法  {% function_name %}
# 这种方式可以将业务逻辑以外的代码放在额外的文件里面，而无需都放在view函数里面


@register.simple_tag   # 下面是自定义的simple_tag标签
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')  # 参数确定所渲染的模板文件，数据将会返回到模板文件。 在其他模板文件调用函数的时候，返回的其实是此处的模板文件
def latest_articles(n=5):  # 可以在模板出自己定义参数
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {'latest_articles': latest_articles}


@register.assignment_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]
                               # annotate 就是对queryset的每一个对象进行注解（增加一个键值对）
                               # 此处的注解就是 统计每一个文章的评论数目
                               # 对queryset进行排序，按照成员的 total_comments来排名


@register.filter(name='markdown')   # 自定义一个filter选择器，这里的name是对下面的函数名重命名。这个选择的作用是将markdown语法解析为html代码
def markdown_filter(text):  # text是等待被传入的字符窜
    return mark_safe(markdown.markdown(text))

