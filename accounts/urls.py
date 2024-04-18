from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('user/', views.user_info, name="userinfo"),
    path('user/follower/', views.follower, name="follower"),
    path('user/following/', views.following, name="following"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('join/', views.join, name="join"),
    path('delete/', views.delete, name="delete"),
    path('follow/<int:user_id>', views.follow, name="follow"),
]
