# Generated by Django 3.1.2 on 2020-11-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='repost_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
