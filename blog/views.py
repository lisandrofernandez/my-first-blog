from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', primary_key=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', primary_key=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    post.publish()
    return redirect('blog.views.post_detail', primary_key=primary_key)

@login_required
def post_remove(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    post.delete()
    return redirect('blog.views.post_list')

def add_comment_to_post(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', primary_key=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, primary_key):
    comment = get_object_or_404(Comment, pk=primary_key)
    comment.approve()
    return redirect('blog.views.post_detail', primary_key=comment.post.pk)

@login_required
def comment_remove(request, primary_key):
    comment = get_object_or_404(Comment, pk=primary_key)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', primary_key=post_pk)
