from django.conf import settings
from django.db import models
from PIL import Image


class Photo(models.Model):
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True)  # Ajout de la date de création

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def __str__(self):
        return f"Photo uploaded by {self.uploader}"


class BlogContributor(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('contributor', 'blog')


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    word_count = models.IntegerField(null=True, blank=True)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')
    starred = models.BooleanField(default=False)  # Ajout du champ 'starred'
    created_at = models.DateTimeField(
        auto_now_add=True)  # Ajout de la date de création

    def _get_word_count(self):
        return len(self.content.split())

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
