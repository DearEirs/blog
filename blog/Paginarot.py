# -*- encoding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger#分页
def Paginat(req,postsAll):
    paginator = Paginator(postsAll,2)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return  posts
