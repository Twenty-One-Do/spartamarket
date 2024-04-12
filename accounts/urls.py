from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('user/<str:user_name>/', views.user_info, name="userinfo"),
    path('user/follower/<str:user_name>/', views.follower, name="follower"),
    path('user/following/<str:user_name>/', views.following, name="following"),
    path('login/', views.login, name="login"),
    path('join/', views.join, name="join"),
]
