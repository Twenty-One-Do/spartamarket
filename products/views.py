from django.shortcuts import render

def post(request):
    return render(request, "post.html")

def write(request):
    return render(request, "write.html")