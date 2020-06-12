from django.db import models
from django.conf import settings
from actors.models import Actor

# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    original_title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_path = models.TextField()
    release_data = models.CharField(max_length=200)
    actors = models.ManyToManyField(Actor, related_name='movies', through='MovieActor')
    
class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

class Review(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

class ReviewComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')