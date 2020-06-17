from django.db import models
from django.conf import settings

from actors.models import Actor

import datetime

from datetime import datetime
from pytz import utc

class Article(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_path = models.CharField(max_length=1000, null=True)
    # image_path = models.CharField(max_length=1000, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='articles')
    username = models.CharField(max_length=200, default='default_username')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles', through='ArticleLike')

    @property
    def popularity(self):
        now = datetime.utcnow()
        during_time = (utc.localize(now)-self.created_at).total_seconds()+3600
        return (self.like_users.count() + 1)/during_time

class ArticleLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class ArticleComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=200, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')