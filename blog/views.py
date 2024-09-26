from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import formset_factory
from . import forms
from . import models
from PIL import Image
from django.contrib.auth import get_user_model
from .forms import FollowUsersForm  # Assurez-vous que cet import est présent


User = get_user_model()


class FollowUsersView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = FollowUsersForm
    template_name = 'blog/follow_users_form.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def test_func(self):
        # Seuls les utilisateurs ayant le rôle 'SUBSCRIBER' peuvent accéder à cette page
        return self.request.user.role == 'SUBSCRIBER'

    def handle_no_permission(self):
        # Rediriger vers la page d'accueil avec un message d'erreur au lieu d'un 403
        return redirect('home')

    def get_object(self, queryset=None):
        # Récupérer automatiquement l'utilisateur connecté
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home')


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/home.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = models.Photo.objects.all()
        context['blogs'] = models.Blog.objects.all()
        return context


class BlogAndPhotoUploadView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'blog/create_blog_post.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'blog.add_photo'

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
            # Sauvegarder la photo
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            # Sauvegarder le blog
            blog = blog_form.save(commit=False)
            blog.photo = photo
            blog.author = request.user
            blog.save()

            # Ajouter l'utilisateur connecté comme contributeur
            blog.contributors.add(request.user, through_defaults={
                                  'contribution': 'Auteur principal'})

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


class BlogUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = models.Blog
    form_class = forms.BlogForm
    template_name = 'blog/edit_blog.html'
    context_object_name = 'blog'
    login_url = '/login/'
    pk_url_kwarg = 'blog_id'
    success_url = reverse_lazy('home')
    permission_required = 'blog.change_blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_form'] = forms.DeleteBlogForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'edit_blog' in request.POST:
            return super().post(request, *args, **kwargs)
        elif 'delete_blog' in request.POST:
            return self.delete(request, *args, **kwargs)


class BlogDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = models.Blog
    template_name = 'blog/delete_blog_confirm.html'
    pk_url_kwarg = 'blog_id'
    success_url = reverse_lazy('home')
    permission_required = 'blog.delete_blog'


class CreateMultiplePhotosView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'blog/create_multiple_photos.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'blog.add_photo'

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
