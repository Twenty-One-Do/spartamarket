from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q
from accounts.models import UserProfile
from products.models import Posts
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


sort_query_dict = {
    "latest": ["-created_at", "최신순", "가장 최신의 중고 물품을 찾아보세요!"],
    "old": ["created_at", "오래된순", "가장 오래된 중고 물품을 찾아보세요!"],
    "popular": ["-likes_num", "인기순", "가장 인기있는 중고 물품을 찾아보세요!"],
    "views": ["-views_num", "조회순", "가장 많이 조회된 중고 물품을 찾아보세요!"],
}

@require_GET
def main(request, sort_by="latest"):

    try:
        order_by = sort_query_dict[sort_by][0]
    except KeyError:
        return redirect('main:home')

    posts_list = Posts.objects.all().order_by(order_by, 'title')
    context={
        "sort_by":sort_query_dict[sort_by][1],
        "sort_by_desc":sort_query_dict[sort_by][2],
        "posts":posts_list[:6],
        "sort_by_q":sort_by,
    }
    return render(request, "main/cards.html", context)

@require_GET
def search(request):
    sq = request.GET.get("search_query")
    searched_posts = Posts.objects.filter(Q(title__icontains=sq)|\
            Q(body__icontains=sq)|\
            Q(user_id__user__username__icontains=sq))

    res_ids = []
    if searched_posts.exists:
        for sp in searched_posts:
            res_ids.append(sp.id)

    return JsonResponse({ "res_ids":res_ids })

def load_more(request):
    page = request.GET.get('page')
    sort_by = request.GET.get('sort_by')
    no_more = False
    try:
        order_by = sort_query_dict[str(sort_by)][0]
    except KeyError:
        return redirect('main:home')

    posts_list = Posts.objects.all().order_by(order_by, 'title')

    paginator = Paginator(posts_list, 6)
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'has_more': False})
    context={
        "sort_by":sort_query_dict[sort_by][1],
        "sort_by_desc":sort_query_dict[sort_by][2],
        "posts":posts_list,
    }

    return render(request, 'main/cards_piece.html', context)