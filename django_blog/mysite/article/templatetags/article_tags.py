# coding=utf-8
from django import template      # 跟模板有关的类和方法

register = template.Library()       #变量名称就是register
from article.models import ArticlePost

# 这个文件的作用是可以在 模板中引用这里的方法  {% function_name %}
# 这种方式可以将业务逻辑以外的代码放在额外的文件里面，而无需都放在view函数里面


@register.simple_tag   # 下面是自定义的simple_tag标签
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()

