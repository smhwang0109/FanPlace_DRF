from django.contrib import admin
from .models import Movie, Genre, MovieActor, MovieGenre, Review, ReviewComment

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieActor)
admin.site.register(MovieGenre)
admin.site.register(Review)
admin.site.register(ReviewComment)