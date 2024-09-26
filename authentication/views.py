from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, UploadProfilePhotoForm
from django.contrib.auth.models import User

# Vue pour l'inscription avec une classe générique


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Auto-login après l'inscription
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Vue pour uploader la photo de profil
class UploadProfilePhotoView(LoginRequiredMixin, UpdateView):
    form_class = UploadProfilePhotoForm
    template_name = 'authentication/upload_profile_photo.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        # Récupère l'utilisateur connecté pour la mise à jour de la photo de profil
        return self.request.user
