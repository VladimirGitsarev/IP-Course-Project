from django.db import models
from django.contrib.auth.models import User
from hashlib import md5
import datetime

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    location = models.CharField(max_length=100, default=None, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    link = models.CharField(max_length=300, default=None, null=True, blank=True)
    status = models.CharField(max_length=300, default=None, null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, default=None, blank=True, related_name='followers')

    def avatar(self):
        digest = md5(self.user.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 150)

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    body = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.datetime.now)
    likes = models.ManyToManyField(User, related_name='post_likes')
    dislikes = models.ManyToManyField(User, related_name='post_dislikes')
    repost_id = models.IntegerField(default=None, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.datetime.now)
