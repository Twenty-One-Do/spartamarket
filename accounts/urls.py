from . import views

urlpatterns = [
    path('/user/<str:user_name>', view.user_info, name="userinfo"),
    path('/user/follower/<str:user_name>', view.follower, name="follower"),
    path('/user/following/<str:user_name>', view.following, name="following"),
    path('/login', view.login, name="login"),
    path('/join', view.join, name="join"),
]
