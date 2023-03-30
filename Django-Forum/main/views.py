from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import *
from main.models import Forum, Thread,ForumUser, Post, Subscription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models.signals import post_save
from django.dispatch import receiver



class ForumList(ListView):
    model = Forum
class ThreadList(ListView):
    model = Thread
class PostList(ListView):
    model = Post



def homepage(request):
    return render(request, 'base_generic.html')



def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'registration/login.html') 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('homepage')

@login_required
def create_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.creator = request.user
            forum.save()
            return redirect('forum_list')
    else:
        form = ForumForm()
    return render(request, 'manipulation/create_forum.html', {'form': form})

@login_required
def create_thread(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.forum = forum
            thread.save()
            return redirect('thread_list')
    else:
        form = ThreadForm()

    context = {
        'forum': forum,
        'form': form,
    }

    return render(request, 'manipulation/create_thread.html', context)

@login_required
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.save()
        return redirect('post_list')
    return render(request, 'manipulation/create_post.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Post
from .forms import PostForm


@login_required
def edit_post(request, thread_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'manipulation/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id, thread_id):
    post = get_object_or_404(Post, id=post_id)
    thread_id = post.thread.id
    post.delete()
    return redirect('post_list')


def filtered_thread_list(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    thread_list = Thread.objects.filter(forum=forum)
    return render(request, 'filters/filtered_threads.html', {'thread_list': thread_list})

def filtered_post_list(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    post_list = Post.objects.filter(thread=thread)
    return render(request, 'filters/filtered_posts.html', {'post_list': post_list})



@login_required
def delete_forum(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    forum.delete()
    return redirect('forum_list')


def delete_thread(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    forum_id = thread.forum.id
    thread.delete()
    return redirect('thread_list')
