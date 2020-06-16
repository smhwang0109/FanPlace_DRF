from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('myaccount/', views.MyAccountView.as_view(), name='my_account'),
    path('<user_pk>/', views.UserDetailView.as_view(), name='profile'),
    path('follow/<int:to_user_pk>/', views.UserFollowView.as_view(), name='user_follow'),
    path('search/<str:keyword>/', views.UserSearchView.as_view(), name='user_search')
]