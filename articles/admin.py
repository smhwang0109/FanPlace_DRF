from django.contrib import admin
from .models import Article, ArticleLike, ArticleComment

admin.site.register(Article)
admin.site.register(ArticleLike)
admin.site.register(ArticleComment)