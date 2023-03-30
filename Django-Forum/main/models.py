from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Forum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name

class Thread(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ForumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    subscriptions = models.ManyToManyField(Forum, related_name='subscribers')

    def __str__(self):
        return self.username




class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    


    def __str__(self):
        return self.body[:50] + '...'


class Subscription(models.Model):
    user = models.OneToOneField(ForumUser, on_delete=models.CASCADE, related_name='forum_user')
    forum = models.OneToOneField(Forum, on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.forum.name}"