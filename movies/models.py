from django.db import models
from django.conf import settings
from actors.models import Actor

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    kr_genre = models.CharField(max_length=200, default='')
    en_genre = models.CharField(max_length=200, default='')

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    original_title = models.CharField(max_length=200, null=True, default='제목이 없습니다. :(')
    overview = models.TextField(null=True, blank=True, default='영화 설명이 없습니다. :(')
    poster_path = models.TextField(null=True, default='noposter')
    release_date = models.CharField(max_length=200, null=True, default='9999-99-99')
    popularity = models.FloatField(null=True, default=0)
    actors = models.ManyToManyField(Actor, related_name='movies', through='MovieActor')
    genres = models.ManyToManyField(Genre, related_name='movies', through='MovieGenre')

class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.CharField(max_length=200)

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    kr_genre = models.CharField(max_length=200)
    en_genre = models.CharField(max_length=200)

class Review(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

class ReviewComment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=200, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')