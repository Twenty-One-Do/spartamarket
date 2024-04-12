from django.urls import path
from . import views

app_name="products"

urlpatterns = [
    path('post/<int:post_id>/', views.post, name="post"),
    path('wirte/', views.write, name="write"),
]