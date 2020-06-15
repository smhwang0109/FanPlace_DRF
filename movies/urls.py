from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view()),
    path('<int:actorId>/', views.ActorMovieListView.as_view()),
    path('<int:movie_pk>/reviews/', views.ReviewListView.as_view()),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.ReviewDetailView.as_view()),
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/', views.ReviewCommentListView.as_view()),
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', views.ReviewCommentDetailView.as_view()),
]