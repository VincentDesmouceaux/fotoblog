from django.urls import path
from django.contrib.auth.views import LoginView
from authentication.views import logout_user

urlpatterns = [
    path('', LoginView.as_view(
        template_name='authentication/login.html',  # Le gabarit de connexion
        redirect_authenticated_user=True),  # Redirige les utilisateurs déjà connectés
        name='login'),
    path('logout/', logout_user, name='logout'),  # Vue pour se déconnecter
]
