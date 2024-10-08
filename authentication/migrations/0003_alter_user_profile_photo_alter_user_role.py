# Generated by Django 5.1.1 on 2024-09-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20240926_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('CREATOR', 'Creator'), ('SUBSCRIBER', 'Subscriber')], default='SUBSCRIBER', max_length=10),
        ),
    ]
