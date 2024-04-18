from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from .forms import PostForm
from .models import Posts, ViewRelationship, LikeRelationship, Tags, TagRelationship
from accounts.models import FollowRelationship

import json, re
pattern = re.compile(r'^[가-힣#]+$')

@require_GET
def post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    follow_user = False
    if request.user.is_authenticated:
        view_rel, create = ViewRelationship.objects.get_or_create(user_id=request.user.userprofile, post_id=post)
        if create:
            post.views_num = F("views_num") + 1
            post.save()
            post.refresh_from_db()
        else:
            view_rel.save()
        follow_rel = FollowRelationship.objects.filter(follower=request.user.userprofile.user_id,\
                                        following=post.user_id_id )
        if follow_rel.exists():
            follow_user = True
    context={
        "tags":post.tags.all(),
        "post":post,
        "writer":post.user_id,
        "follow_user":follow_user,
    }
    return render(request, "products/post.html", context)

@require_http_methods(["GET", "POST"])
@login_required
def write(request):
    if request.method == "GET":
        form = PostForm()
        context = {
            "form":form
        }
        return render(request, "products/write.html", context)
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        tags = request.POST.get("tags").replace(" ","")
        if (bool(pattern.match(tags)) or tags=="") and form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.userprofile
            post.save()

            if tags!="":
                for tag in tags.split("#")[1:]:
                    tag_rel_ins = TagRelationship()
                    tag_ins, created = Tags.objects.get_or_create(name=tag)
                    tag_rel_ins.tag_id = tag_ins
                    tag_rel_ins.post_id = post
                    tag_rel_ins.save()
            
            return redirect("products:post", post.id)
        return redirect("products:write")

@require_POST
@login_required
def like(request):
    data = json.loads(request.body)
    user = request.user.userprofile
    post = get_object_or_404(Posts, id=data.get("post_id"))
    inst, like_created = LikeRelationship.objects.get_or_create(user_id=user,post_id=post)
    if not like_created: # 이미 좋아요를 눌렀던 포스트
        post.likes_num = F('likes_num')-1
        inst.delete()
    else: # 새로 좋아요를 눌렀던 포스트
        post.likes_num = F('likes_num')+1
    post.save()
    post.refresh_from_db()
    new_like_num = post.likes_num
    print(post)
    return JsonResponse({'new_like_num': new_like_num, 'already_like': not like_created})

@require_POST
@login_required
def delete(request, post_id):
    user = request.user.userprofile
    post = get_object_or_404(Posts,id=post_id)
    if post.user_id==user:
        post.delete()
    return redirect("main:home")