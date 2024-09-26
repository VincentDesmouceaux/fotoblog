from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from . import forms
from . import models
from PIL import Image


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/home.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = models.Photo.objects.all()
        context['blogs'] = models.Blog.objects.all()
        return context


class BlogAndPhotoUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/create_blog_post.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        blog_form = forms.BlogForm()
        photo_form = forms.PhotoForm()
        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)

        if blog_form.is_valid() and photo_form.is_valid():
            # Sauvegarde du blog et de la photo
            photo = photo_form.save(commit=False)
            photo.uploader = request.user

            # Redimensionner l'image avec Pillow
            img = Image.open(photo.image)
            img = img.resize((800, 800))
            img.save(photo.image.path)

            photo.save()

            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()

            return redirect('home')

        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,
        }
        return self.render_to_response(context)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = models.Blog
    template_name = 'blog/view_blog.html'
    context_object_name = 'blog'
    login_url = '/login/'
    pk_url_kwarg = 'blog_id'


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Blog
    form_class = forms.BlogForm
    template_name = 'blog/edit_blog.html'
    context_object_name = 'blog'
    login_url = '/login/'
    pk_url_kwarg = 'blog_id'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_form'] = forms.DeleteBlogForm()
        return context

    def post(self, request, *args, **kwargs):
        # Gestion des deux types de formulaires (édition et suppression)
        if 'edit_blog' in request.POST:
            return super().post(request, *args, **kwargs)
        elif 'delete_blog' in request.POST:
            # Gérer la suppression dans la vue de mise à jour
            return self.delete(request, *args, **kwargs)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Blog
    template_name = 'blog/delete_blog_confirm.html'
    pk_url_kwarg = 'blog_id'
    success_url = reverse_lazy('home')


# Nouvelle vue pour le téléchargement multiple de photos
class CreateMultiplePhotosView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/create_multiple_photos.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
        formset = PhotoFormSet()
        return self.render_to_response({'formset': formset})

    def post(self, request, *args, **kwargs):
        PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
        formset = PhotoFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')

        return self.render_to_response({'formset': formset})
