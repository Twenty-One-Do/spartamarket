from django.shortcuts import render

# Create your views here.
def user_info(request):
    return render(request, "accounts/user_info.html")

def follower(request):
    return render(request, "accounts/follower.html")

def following(request):
    return render(request, "accounts/following.html")

def login(request):
    return render(request, "accounts/login.html")

def join(request):
    return render(request, "accounts/join.html")