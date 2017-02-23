# -*- encoding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from models import Post
# Create your views here.
from .forms import Postform
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger#分页
from django.contrib.auth.decorators import login_required#登录
from blog.models import Tag,Category
from django.db.models import Count
from blog.Paginarot import Paginat


def post_list(req):
    postsAll = Post.objects.filter(published_date__isnull=False)
    posts = Paginat(req,postsAll)
    tags = Tag.objects.all()
    cg = Category.objects.all()
    postsAll = postsAll.order_by("-published_date")
    return  render(req,'blog/post_list.html',{'postsAll':postsAll,'posts':posts,'page':True,'tags':tags,'cgs':cg})

def post_detail(req,pk):
    post = get_object_or_404(Post,pk=pk)
    postsAll = Post.objects.filter(published_date__isnull=False).order_by("-published_date")
    tags = Tag.objects.all()
    return  render(req,'blog/post_detail.html',{'post':post,'postsAll':postsAll,'tags':tags})

@login_required
def post_new(req):
    if req.method=='POST':
        form = Postform(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            return  redirect('blog.views.post_detail',pk=post.pk)
    else:
        form = Postform()
    return  render(req,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(req,pk):
    post = get_object_or_404(Post, pk=pk)
    if req.method=='POST':
        form = Postform(req.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            ptags = req.POST['tags'].strip()
            all_tags = []
            if ptags:
                tags = ptags.split(',')
                for tag in tags:
                    try:
                        t = Tag.objects.get(name=tag)
                    except Tag.DoesNotExist:
                        t = Tag(name=tag)
                        t.save()
                    all_tags.append(t)
            post.save()
            post.tags.clear()
            for i  in all_tags:
                post.tags.add(i)
            #Tag.objects.annotate(num_post=Count('post')).filter(num_post=0).delete()
            return  redirect('blog.views.post_detail',pk=post.pk)
    else:
        form = Postform(instance=post)
    return render(req,'blog/post_edit.html',{'form':form})

def post_draft_list(req):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return  render(req,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(req,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return  redirect('blog.views.post_detail',pk=pk)

def post_remove(req,pk):
    post  = get_object_or_404(Post,pk=pk)
    post.delete()
    return  redirect('blog.views.post_list')

def about_me(req):
    postsAll = Post.objects.filter(published_date__isnull=False).order_by("-published_date")
    tags = Tag.objects.all()
    return  render(req,'blog/about_me.html',{'postsAll':postsAll,'tags':tags})

def contents(req):
    postsAll = Post.objects.filter(published_date__isnull=False).order_by("-published_date")
    tags = Tag.objects.all()
    return  render(req,'blog/contents.html',{'postsAll':postsAll,'tags':tags})

def post_list_by_tag(req,tag):
    posts = Post.objects.annotate(num_comment=Count('author')).filter(
        published_date__isnull=False, tags__name=tag).prefetch_related(
        'category').prefetch_related('tags').order_by('-published_date')
    posts = Paginat(req,posts)
    postsAll = Post.objects.filter(published_date__isnull=False).order_by("-published_date")
    tags = Tag.objects.all()
    return render(req, 'blog/post_list.html',
                  {'posts': posts, 'list_header': '文章标签 \'{}\''.format(tag),'page':True,'postsAll':postsAll,'tags':tags})

def post_list_by_category(req,cg):
    posts = Post.objects.annotate(num_comment=Count('author')).filter(
        published_date__isnull=False,category__name=cg).prefetch_related(
        'category').prefetch_related('tags').order_by('-published_date')
    posts = Paginat(req, posts)
    return  render(req,'blog/post_list.html',{'posts':posts,'list_header':'文章标签\'{}\''.format(cg),'page':True})

