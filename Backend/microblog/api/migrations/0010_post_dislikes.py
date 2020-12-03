# Generated by Django 3.1.2 on 2020-11-16 20:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(related_name='post_dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]