from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.


from .models import *

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'description']

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']
        labels = {
            'title': 'Title'
        }

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Post
        fields = ['body']