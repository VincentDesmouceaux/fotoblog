from django.db.models import Q, Value, CharField
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import formset_factory
from itertools import chain
from operator import attrgetter
from . import forms
from . import models
from django.contrib.auth import get_user_model
from .forms import FollowUsersForm
from .models import Photo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
User = get_user_model()


class PhotoFeedView(LoginRequiredMixin, ListView):
    model = models.Photo
    template_name = 'blog/photo_feed.html'
    context_object_name = 'photos'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    paginate_by = 4  # Nombre de photos par page

    def get_queryset(self):
        # Récupérer les photos dont le téléverseur est suivi par l'utilisateur connecté, ou les photos de l'utilisateur lui-même
        return models.Photo.objects.filter(
            Q(uploader__in=self.request.user.follows.all()) | Q(
                uploader=self.request.user)
        ).order_by('-created_at')


class FollowUsersView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = FollowUsersForm
    template_name = 'blog/follow_users_form.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.role == 'SUBSCRIBER'

    def handle_no_permission(self):
        return redirect('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home')


class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'blog/home.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    paginate_by = 4  # Nombre d'éléments par page

    def get_queryset(self):
        # Récupérer les blogs des contributeurs suivis, blogs mis en avant, ou les blogs auxquels l'utilisateur a contribué
        blogs = models.Blog.objects.filter(
            Q(contributors__in=self.request.user.follows.all()) | Q(
                starred=True) | Q(contributors=self.request.user)
        ).annotate(type=Value('Blog', output_field=CharField()))

        # Récupérer les photos des utilisateurs suivis ou les photos de l'utilisateur lui-même
        photos = models.Photo.objects.filter(
            Q(uploader__in=self.request.user.follows.all()) | Q(
                uploader=self.request.user)
        ).exclude(blog__in=blogs).annotate(type=Value('Photo', output_field=CharField()))

        # Combiner les deux querysets dans une liste et trier par date de création
        combined_list = sorted(
            chain(blogs, photos),
            key=attrgetter('created_at'),
            reverse=True
        )

        return combined_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les éléments combinés
        combined_list = self.get_queryset()

        # Pagination
        paginator = Paginator(combined_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            combined_list = paginator.page(page)
        except PageNotAnInteger:
            # Si la page n'est pas un entier, retourne la première page
            combined_list = paginator.page(1)
        except EmptyPage:
            # Si la page est hors des limites, retourne la dernière page valide
            combined_list = paginator.page(paginator.num_pages)

        context['combined_list'] = combined_list
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
