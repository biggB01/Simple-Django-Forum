from django.urls import path,include
from . import views
from main.views import *


urlpatterns = [
    path('', homepage, name='homepage'),
    path('forums', ForumList.as_view(), name='forum_list'),
    path('threads', ThreadList.as_view(), name='thread_list'),
    path('posts', PostList.as_view(), name='post_list'),
    path('login', login_request, name='login'),
    path('register', register, name='register'),
    path('logout', logout_request, name='logout'),
    path('create_forum/', views.create_forum, name='create_forum'),
    path('create_thread/<int:forum_id>/', views.create_thread, name='create_thread'),
    path('threads/<int:thread_id>/posts/create/', views.create_post, name='create_post'),
    path('threads/<int:thread_id>/posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('threads/<int:thread_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('forums/<int:forum_id>/threads/', views.filtered_thread_list, name='filtered_thread_list'),
    path('forums/<int:thread_id>/posts/', views.filtered_post_list, name='filtered_post_list'),
    path('forums/<int:forum_id>/delete/', delete_forum, name='delete_forum'),
    path('threads/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('threads/<int:thread_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
]
