from django.shortcuts import render
from django.http import JsonResponse
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post, Account, Comment
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostAddSerializer, AccountSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            acc = Account.objects.create(user=user)
            acc.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'All Posts List':'/posts/',
        'One Post':'/posts/<str:pk>',
        'Create Post':'/post/new/',
        'Delete Post':'/posts/delete/<str:pk>',
        'Create User':'/create/',
        'Edit User': '/user/edit/<str:pk>',
        'One User': '/user/<str:username>' 
    }
    return Response(api_urls)

@api_view(['GET'])
def current_user(request):
    acc = Account.objects.get(user=request.user)
    serializer = AccountSerializer(acc)
    return Response(serializer.data)

@api_view(['GET'])
def post_list(request):
    user = User.objects.get(username=request.user)
    acc = Account.objects.get(user=user)
    ids = list(acc.following.all())
    ids.append(user.id)
    posts = Post.objects.filter(user__in=ids).order_by('-date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_post(request):
    data =  {
            'user':request.data['user'],
            'body':request.data['body']
        }
    serializer = PostAddSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post)

    return Response(serializer.data)


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(id=pk)
    user = User.objects.get(username=request.user) 
    if request.data['liked']:
        post.likes.remove(user)
    else:
        post.dislikes.remove(user)
        post.likes.add(user)
    post.save()
    serializer = PostSerializer(post)

    return Response(serializer.data)

@api_view(['POST'])
def post_dislike(request, pk):
    post = Post.objects.get(id=pk)
    user = User.objects.get(username=request.user)
    if request.data['disliked']:
        post.dislikes.remove(user)
    else: 
        post.likes.remove(user)
        post.dislikes.add(user)
    post.save()
    serializer = PostSerializer(post)

    return Response(serializer.data)

@api_view(['GET'])
def user_posts(request, pk, count):

    acc = Account.objects.get(user=User.objects.get(id=pk))
    if count != 'all':
        posts = acc.post_set.all().order_by('-date')[:int(count)]
    else:
        posts = acc.post_set.all().order_by('-date')
    serializer = PostSerializer(posts, many=True)
    
    return Response(serializer.data)
    
@api_view(['GET'])
def user(request, username):
    acc = Account.objects.get(user=User.objects.get(username=username))
    serializer = AccountSerializer(acc)

    return Response(serializer.data)

@api_view(['POST'])
def user_follow(request, pk):
    acc = Account.objects.get(user=pk)
    follower = Account.objects.get(user=request.data['user'])
    if request.data['followed']:
        acc.followers.remove(follower)
    else:
        acc.followers.add(follower)
    acc.save()

    serializer = AccountSerializer(acc)

    return Response(serializer.data)

@api_view(['GET'])
def post_comments(request, pk):
    comments = Comment.objects.filter(post=pk).order_by('-date')
    serializer = CommentSerializer(comments, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def new_comment(request, pk):
    comment = Comment.objects.create(
        post=Post.objects.get(id=pk), 
        user=Account.objects.get(user=User.objects.get(username=request.user)),
        body=request.data['body']
        )
    comment.save()
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(['POST'])
def user_edit(request, pk):
    account = Account.objects.get(user=pk)
    user = User.objects.get(id=pk)
    user.email = request.data['email']
    user.first_name = request.data['first_name']
    user.last_name = request.data['last_name']
    user.username = request.data['username']
    account.status = request.data['status']
    account.location = request.data['location']
    account.link = request.data['link']
    account.birthdate = request.data['birthdate']
    user.save()
    account.save()
    serializer = AccountSerializer(account)

    return Response(serializer.data)

@api_view(['POST'])
def new_repost(request, pk):
    user = User.objects.get(username=request.user)
    data =  {
            'user':user.id,
            'body':request.data['body'],
            'repost_id':pk
        }
    serializer = PostAddSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_post(request, pk):

    post = Post.objects.get(id=pk)
    post.delete()

    return Response("Post {} deleted.".format(pk))

@api_view(['GET'])
def popular_users(request):
    user = User.objects.get(username=request.user)
    accounts = list(Account.objects.all().exclude(user=user))[:5]
    random.shuffle(accounts)
    serizalier = AccountSerializer(accounts, many=True)
    return Response(serizalier.data)

@api_view(['GET'])
def user_followers(request):
    user = User.objects.get(username=request.user)
    acc = Account.objects.get(user=user)
    print()
    serializer = AccountSerializer(acc.followers.all(), many=True)
    return Response(serializer.data)

@api_view(['POST'])
def search(request):
    
    users = User.objects.filter(username__startswith=request.data['query'])
    accounts = Account.objects.filter(user__in=users)
    posts = Post.objects.filter(body__icontains=request.data['query'])
    serialiser_acc = AccountSerializer(accounts, many=True)
    serialiser_posts = PostSerializer(posts, many=True)
    
    return Response({'users':serialiser_acc.data, 'posts':serialiser_posts.data})