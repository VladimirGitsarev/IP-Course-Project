from rest_framework import serializers
from .models import Post, Account, Comment
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password':{'write_only':True, 'required':True}}
    
    def create(self, data):
        print('data:', data)
        password = data.pop('password', None)
        instance = self.Meta.model(**data)
        if password is not None:
            instance.set_password(password)
        print(instance)
        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    img = serializers.CharField(source='avatar', read_only=True)
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_followers(self, obj):
        ids = [ acc.user.id for acc in obj.followers.all()]
        return ids

class CommentSerializer(serializers.ModelSerializer):

    user = AccountSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1

class PostSerializer(serializers.ModelSerializer):

    user = AccountSerializer()
    comments = serializers.SerializerMethodField()
    repost = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        depth = 1

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj.id)
        # serializer = CommentSerializer(comments, many=True)
        # return serializer.data
        return len(comments)

    def get_repost(self, obj):
        if obj.repost_id:
            post = Post.objects.get(id=obj.repost_id)
            serializer = PostSerializer(post)
            return serializer.data

    def get_reposts_count(self, obj):
        reposts = Post.objects.filter(repost_id=obj.id)
        return len(reposts)

class PostAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'user', 'body', 'date', 'repost_id']
        
