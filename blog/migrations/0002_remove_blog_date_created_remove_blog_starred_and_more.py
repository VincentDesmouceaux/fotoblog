# Generated by Django 5.1.1 on 2024-09-26 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='starred',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.photo'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
