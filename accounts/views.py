from django.shortcuts import render

# Create your views here.
def user_info(request):
    return render(request, "user_info.html")

def follower(request):
    return render(request, "follower.html")

def following(request):
    return render(request, "following.html")

def login(request):
    return render(request, "login.html")

def join(request):
    return render(request, "join.html")