from django.urls import path
from . import views

app_name="main"

urlpatterns = [
    path('', views.main, name="home"),
    path('/<str:sort_by>', views.main, name="home"),
    path('search/', views.search, name="search"),
    path('load_more/', views.load_more)
]
