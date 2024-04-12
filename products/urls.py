from . import views

urlpatterns = [
    path('/post/<int:post_id>', views.post, name="post"),
    path('/wirte', views.write, name="write"),
]