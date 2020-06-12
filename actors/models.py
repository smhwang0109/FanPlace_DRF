from django.db import models
from django.conf import settings

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    birthday = models.CharField(max_length=20)
    deathday = models.CharField(max_length=20)
    gender = models.IntegerField()
    profile_path = models.CharField(max_length=200)
    popularity = models.IntegerField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_actors', through='ActorLike')

class ActorLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)