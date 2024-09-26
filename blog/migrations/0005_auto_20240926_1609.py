from django.db import migrations


def migrate_author_to_contributors(apps, schema_editor):
    Blog = apps.get_model('blog', 'Blog')
    BlogContributor = apps.get_model('blog', 'BlogContributor')

    for blog in Blog.objects.all():
        if blog.author:
            # Ajoutez l'auteur comme contributeur avec la contribution par défaut
            BlogContributor.objects.create(
                blog=blog,
                contributor=blog.author,
                contribution='Auteur principal'
            )


class Migration(migrations.Migration):

    dependencies = [
        # Nom correct de la dernière migration
        ('blog', '0004_alter_blog_author_blogcontributor_blog_contributors'),
    ]

    operations = [
        migrations.RunPython(migrate_author_to_contributors),
    ]
