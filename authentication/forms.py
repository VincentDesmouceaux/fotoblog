from django.contrib.auth.forms import UserCreationForm
from django import forms
# Assurez-vous que cela fait référence à votre modèle User personnalisé
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User  # Utilisez votre modèle User personnalisé
        fields = ['username', 'email', 'first_name', 'last_name', 'role']


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = User()
        fields = ['profile_photo']
