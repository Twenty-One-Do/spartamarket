from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import UserProfile, FollowRelationship
from products.models import Posts, LikeRelationship, ViewRelationship
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
@login_required
@require_http_methods(["GET", "POST"])
def user_info(request):
    user = request.user.userprofile
    if request.method =="GET":

        users_posts = Posts.objects.filter(user_id=user)
        paginator = Paginator(users_posts, 3)
        page_mypost = request.GET.get('page_mypost', 1)
        try:
            users_posts = paginator.page(page_mypost)
        except PageNotAnInteger:
            users_posts = paginator.page(1)
        except EmptyPage:
            users_posts = paginator.page(paginator.num_pages)

        users_likes = LikeRelationship.objects.filter(user_id=user).\
                exclude(post_id__user_id=user).\
                values_list('post_id', flat=True)
        users_likes = Posts.objects.filter(id__in=users_likes)
        paginator = Paginator(users_likes, 3) 
        page_mylike = request.GET.get('page_mylike', 1)
        try:
            users_likes = paginator.page(page_mylike)
        except PageNotAnInteger:
            users_likes = paginator.page(1)
        except EmptyPage:
            users_likes = paginator.page(paginator.num_pages)

        users_views = ViewRelationship.objects.filter(user_id=user).\
                exclude(post_id__user_id=user).\
                order_by('-created_at')
        #users_views = Posts.objects.filter(id__in=users_views)

        paginator = Paginator(users_views, 3)
        page_myview = request.GET.get('page_myview', 1)
        try:
            users_views = paginator.page(page_myview)
        except PageNotAnInteger:
            users_views = paginator.page(1)
        except EmptyPage:
            users_views = paginator.page(paginator.num_pages)

        context = {
            "user":user,
            "users_posts":users_posts,
            "users_likes":users_likes,
            "users_views":users_views,
        }
        return render(request, "accounts/user_info.html", context)
    else:
        image_file = request.FILES['image']
        user.profile_image = image_file
        user.save()
        return JsonResponse({'message': '이미지', 'img_link':user.profile_image.url}, status=200)

def following(request):
    user = request.user.userprofile
    following_ids = FollowRelationship.objects.filter(follower=user).values_list('following', flat=True)
    followers = UserProfile.objects.filter(user__in=following_ids)
    context = {
        "user":user,
        "followings":followers,
    }
    return render(request, "accounts/follower.html", context)

def follower(request):
    user = request.user.userprofile
    follower_ids = FollowRelationship.objects.filter(following=user).values_list('follower', flat=True)
    followings = UserProfile.objects.filter(user__in=follower_ids)
    context = {
        "user":user,
        "followings":followings,
    }
    return render(request, "accounts/following.html", context)

@require_POST
@login_required
def follow(request, user_id):
    you_follow_me = get_object_or_404(UserProfile, user_id=user_id)
    im_following_you = request.user.userprofile
    if im_following_you.user_id != you_follow_me.user_id:
        follow, created = FollowRelationship.objects.get_or_create(follower=im_following_you, following=you_follow_me)

        if not created: # 이미 팔로우한 사용자
            follow.likes_num = F('likes_num')-1
            follow.delete()
            im_following_you.following_num = F('following_num')-1
            you_follow_me.follower_num = F('follower_num')-1
        else: # 새로 좋아요를 눌렀던 포스트
            follow.likes_num = F('likes_num')+1
            im_following_you.following_num = F('following_num')+1
            you_follow_me.follower_num = F('follower_num')+1

        im_following_you.save()
        you_follow_me.save()
        im_following_you.refresh_from_db()
        you_follow_me.refresh_from_db()
        return redirect("accounts:userinfo")
    else:
        return redirect("accounts:userinfo")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context={
            "form":form
        }
        return render(request, "accounts/login.html", context)
    else:
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            next_url = request.GET.get("next") or "main:home"
            return redirect(next_url)
        else:
            return redirect("accounts:login")
        
@require_GET
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("main:home")

@require_http_methods(["GET", "POST"])
def join(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        context = {
            "form":form,
        }
        return render(request, "accounts/join.html", context)
    else:
        form = CustomUserCreationForm(data=request.POST)
        userprofile = UserProfile()
        if form.is_valid():
            user=form.save()
            userprofile.user = user
            userprofile.save()
            auth_login(request,user)
            return redirect("main:home")
        else:
            return redirect("accounts:join")

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
        return redirect("main:home")
    else:
        return redirect("main:home")
