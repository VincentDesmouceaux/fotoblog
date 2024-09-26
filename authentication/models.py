from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('CREATOR', 'Creator'),
        ('SUBSCRIBER', 'Subscriber'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='SUBSCRIBER')

    # Champ pour la photo de profil
    profile_photo = models.ImageField(
        upload_to='profile_photos/', blank=True, null=True)

    # Relation plusieurs-à-plusieurs pour suivre les créateurs
    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': 'CREATOR'},
        symmetrical=False,
        verbose_name='suit'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Attribution automatique des groupes selon le rôle
        if self.role == 'CREATOR':
            group, created = Group.objects.get_or_create(name='creators')
            self.groups.add(group)
        elif self.role == 'SUBSCRIBER':
            group, created = Group.objects.get_or_create(name='subscribers')
            self.groups.add(group)
