from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from blog.views import HomePageView, BlogAndPhotoUploadView, BlogDetailView, BlogUpdateView, BlogDeleteView, CreateMultiplePhotosView, FollowUsersView
from authentication.views import SignupView, UploadProfilePhotoView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='authentication/login.html',
         redirect_authenticated_user=True), name='login'),
    path('', HomePageView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'), name='password_change_done'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('upload-profile-photo/', UploadProfilePhotoView.as_view(),
         name='upload_profile_photo'),
    path('blog/create/', BlogAndPhotoUploadView.as_view(), name='blog_create'),
    path('blog/<int:blog_id>/', BlogDetailView.as_view(), name='view_blog'),
    path('blog/<int:blog_id>/edit/', BlogUpdateView.as_view(), name='edit_blog'),
    path('blog/<int:blog_id>/delete/',
         BlogDeleteView.as_view(), name='delete_blog'),
    path('photo/upload-multiple/', CreateMultiplePhotosView.as_view(),
         name='create_multiple_photos'),  # Nouvelle URL
    path('follow-users/', FollowUsersView.as_view(), name='follow_users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
