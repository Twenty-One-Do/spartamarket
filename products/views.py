from django.shortcuts import render

def post(request):
    return render(request, "products/post.html")

def write(request):
    return render(request, "products/write.html")