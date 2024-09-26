from django import forms
from . import models
from .models import Blog, Photo

from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']


class BlogForm(forms.ModelForm):
    contributors = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='CREATOR'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'contributors']


class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(
        widget=forms.HiddenInput, required=False, initial=False)

    class Meta:
        model = models.Blog
        fields = ['title', 'content']


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo  # Assurez-vous que le modèle Photo existe dans models.py
        # Ajustez les champs en fonction de votre modèle
        fields = ['image', 'caption']
