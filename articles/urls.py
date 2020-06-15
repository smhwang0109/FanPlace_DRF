from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view()),
    path('populars/', views.ArticlePopularListView.as_view()),
    path('<int:actorId>/', views.ActorArticleListView.as_view()),
    path('<int:article_pk>/', views.ArticleDetailView.as_view()),
    path('<int:article_pk>/comments/', views.ArticleCommentListView.as_view()),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.ArticleCommentDetailView.as_view()),
    path('<int:article_pk>/like/', views.ArticleLikeView.as_view()),
    path('search/<str:keyword>/', views.ArticleSearchView.as_view()),
]