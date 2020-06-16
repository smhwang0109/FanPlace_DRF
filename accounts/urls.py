from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<user_pk>/', views.UserDetailView.as_view(), name='profile'),
    path('follow/<int:to_user_pk>/', views.UserFollowView.as_view(), name='user_follow'),
    path('search/<str:keyword>/', views.UserSearchView.as_view(), name='user_search')
]