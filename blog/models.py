from django.conf import settings
from django.db import models
from PIL import Image


class Photo(models.Model):
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)

    # Taille maximale pour le redimensionnement de l'image
    IMAGE_MAX_SIZE = (800, 800)

    # Méthode pour redimensionner l'image
    def resize_image(self):
        image = Image.open(self.image)
        # Conserve les proportions d'origine
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # Sauvegarde de l'image redimensionnée sur le système de fichiers
        image.save(self.image.path)

    # Surcharge de la méthode save pour appeler resize_image
    def save(self, *args, **kwargs):
        # Appel de la méthode save parente pour sauvegarder l'objet Photo
        super().save(*args, **kwargs)
        # Redimensionnement de l'image après l'avoir sauvegardée
        self.resize_image()

    def __str__(self):
        return f"Photo uploaded by {self.uploader}"


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    # Nouveau champ pour stocker le nombre de mots
    word_count = models.IntegerField(null=True, blank=True)

    # Méthode interne pour calculer le nombre de mots dans le contenu
    def _get_word_count(self):
        # Sépare le contenu en mots et renvoie leur nombre
        return len(self.content.split())

    # Surcharge de la méthode save pour mettre à jour le word_count
    def save(self, *args, **kwargs):
        # Avant de sauvegarder, on met à jour le word_count
        self.word_count = self._get_word_count()
        # Appel à la méthode save parent pour sauvegarder l'objet Blog
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
