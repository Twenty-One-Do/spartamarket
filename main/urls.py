from . import views

urlpatterns = [
    path('/', views.main, name="home"),
]
