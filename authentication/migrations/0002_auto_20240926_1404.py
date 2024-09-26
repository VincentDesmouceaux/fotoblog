from django.db import migrations


def create_groups(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Récupérer les permissions pour le modèle Photo
    add_photo = Permission.objects.get(codename='add_photo')
    change_photo = Permission.objects.get(codename='change_photo')
    delete_photo = Permission.objects.get(codename='delete_photo')
    view_photo = Permission.objects.get(codename='view_photo')

    # Créer le groupe creators et lui attribuer les permissions de gestion des photos
    creators = Group(name='creators')
    creators.save()
    creators.permissions.set(
        [add_photo, change_photo, delete_photo, view_photo])

    # Créer le groupe subscribers et lui attribuer uniquement la permission de visualisation
    subscribers = Group(name='subscribers')
    subscribers.save()
    subscribers.permissions.add(view_photo)

    # Ajouter les utilisateurs aux groupes en fonction de leur rôle
    for user in User.objects.all():
        if user.role == 'CREATOR':
            creators.user_set.add(user)
        elif user.role == 'SUBSCRIBER':
            subscribers.user_set.add(user)


class Migration(migrations.Migration):

    dependencies = [
        # Modifiez selon votre dernière migration
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
