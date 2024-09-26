from django.db import migrations


def create_blog_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Récupérer les permissions du modèle Blog
    add_blog = Permission.objects.get(codename='add_blog')
    change_blog = Permission.objects.get(codename='change_blog')
    delete_blog = Permission.objects.get(codename='delete_blog')
    view_blog = Permission.objects.get(codename='view_blog')

    # Récupérer les groupes
    creators = Group.objects.get(name='creators')
    subscribers = Group.objects.get(name='subscribers')

    # Ajouter les permissions aux groupes
    creators.permissions.set([add_blog, change_blog, delete_blog, view_blog])
    subscribers.permissions.set([view_blog])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),  # Dépend de votre fichier initial de migrations
    ]

    operations = [
        migrations.RunPython(create_blog_permissions),
    ]
