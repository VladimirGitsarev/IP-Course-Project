from django.urls import path
from . import views
from rest_framework import routers
from .views import UserViewSet
from django.conf.urls import include
from .views import BlackListTokenView, current_user, UserCreateView

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('', include(router.urls)),
    path('posts/', views.post_list, name='posts-list'),
    path('logout/', BlackListTokenView.as_view(), name='blacklist'),
    path('current_user/', current_user),
    path('create/', UserCreateView.as_view(), name="create-user"),
    path('posts/new/', views.add_post, name="add-post"),
    path('posts/<str:pk>', views.get_post, name="get-post"),
    path('posts/like/<str:pk>', views.post_like, name="like-post"),
    path('posts/dislike/<str:pk>', views.post_dislike, name="dislike-post"),
    path('posts/user/<str:pk>/<str:count>', views.user_posts, name="user-posts"),
    path('posts/comments/<str:pk>', views.post_comments, name="post-comments"),
    path('posts/comments/new/<str:pk>', views.new_comment, name="new-comment"),
    path('posts/repost/<str:pk>', views.new_repost, name="new-repost"),
    path('posts/delete/<str:pk>', views.delete_post, name="delete-post"),
    path('user/<str:username>', views.user, name="user"),
    path('user/follow/<str:pk>', views.user_follow, name="user-follow"),
    path('user/edit/<str:pk>', views.user_edit, name="user-edit"),
    path('user/recommend/get', views.popular_users, name="recommend-users"),
    path('user/followers/get', views.user_followers, name="user-followers"),
    path('search/', views.search, name="search")
]