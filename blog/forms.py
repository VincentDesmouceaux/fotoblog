from django import forms
from . import models


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
