from django.urls import path
from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.ActorListView.as_view()),
    path('populars/', views.ActorPopularListView.as_view()),
    path('<int:actor_pk>/', views.ActorDetailView.as_view()),
    path('<int:actor_pk>/like/', views.ActorLikeView.as_view()),
]