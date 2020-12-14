from django.contrib import admin
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Account, Comment
from django.contrib.auth.models import User

class PostsInstanceInline(admin.TabularInline):
    model = Post

class UsersInstanceInline(admin.TabularInline):
    model = User

class CommentsInstanceInline(admin.TabularInline):
    model = Comment

def make_comments_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_comments_inactive.short_description = "Mark selected comments as inactive"

def make_posts_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_posts_inactive.short_description = "Mark selected posts as inactive"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("body", "user_link", "date", "likes_count", "dislikes_count", "comments_count", "repost", "active", )
    list_filter = ("date", "active", )
    search_fields = ("body__icontains", "user__user__username")
    filter_horizontal = ("likes", "dislikes", )
    actions = (make_posts_inactive, )
    inlines = [CommentsInstanceInline]

    class Meta:
        ordering = ("date")

    def user_link(self, obj):
        url = (
            reverse("admin:api_account_change", kwargs={'object_id': obj.user.user.id})
        )
        return format_html('<a href="{}">{}</a>', url, obj.user.user.username)

    def likes_count(self, obj):
        ids = str([user.id for user in obj.likes.all()]).replace(']', '').replace('[', '')
        url = (
            reverse("admin:api_account_changelist")
            + "?" 
            + urlencode({"user__in": f"{ids}"})
        )
        return format_html('<a href="{}">{} Likes</a>', url, obj.likes.all().count())
        

    def dislikes_count(self, obj):
        ids = str([user.id for user in obj.dislikes.all()]).replace(']', '').replace('[', '')
        url = (
            reverse("admin:api_account_changelist")
            + "?" 
            + urlencode({"user__in": f"{ids}"})
        )
        return format_html('<a href="{}">{} Dislikes</a>', url, obj.dislikes.all().count())

    def repost(self, obj):
        if obj.repost_id:
            url = (
                reverse("admin:api_post_change", kwargs={'object_id':obj.repost_id})
            )
            return format_html('<a href="{}">{}</a>', url, "Yes")
        return 'No'

    def comments_count(self, obj):
        ids = str([user.id for user in Comment.objects.filter(post=obj)]).replace(']', '').replace('[', '')
        url = (
            reverse("admin:api_comment_changelist")
            + "?" 
            + urlencode({"id__in": f"{ids}"})
        )
        return format_html('<a href="{}">{} Comments</a>', url, Comment.objects.filter(post=obj).count())

    user_link.short_description = "User"
    likes_count.short_description = "Likes"
    dislikes_count.short_description = "Dislikes"
    comments_count.short_description = "Comments"

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [PostsInstanceInline, CommentsInstanceInline]
    list_display = ("user", "user_id", "first_name", "last_name", "birthdate", "posts_count", "comments_count", "following_count", "followers_count")
    search_fields = ("user__username__startswith", ) 

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def posts_count(self, obj):
        url = (
            reverse("admin:api_post_changelist")
            + "?" 
            + urlencode({"user__user__exact": f"{obj.user.id}"})
        )
        return format_html('<a href="{}">{} Posts</a>', url, Post.objects.filter(user=obj).count())

    def comments_count(self, obj):
        url = (
            reverse("admin:api_comment_changelist")
            + "?" 
            + urlencode({"user__user__exact": f"{obj.user.id}"})
        )
        return format_html('<a href="{}">{} Comments</a>', url, Comment.objects.filter(user=obj).count())

    def following_count(self, obj):
        url = (
            reverse("admin:api_account_changelist")
            + "?" 
            + urlencode({"followers__user__exact": f"{obj.user.id}"})
        )
        return format_html('<a href="{}">{} Following</a>', url, obj.following.all().count())

    def followers_count(self, obj):
        url = (
            reverse("admin:api_account_changelist")
            + "?" 
            + urlencode({"following__user__exact": f"{obj.user.id}"})
        )
        return format_html('<a href="{}">{} Followers</a>', url, obj.followers.all().count())

    def user_id(self, obj):
        url = (
            reverse("admin:auth_user_change", kwargs={'object_id':obj.user_id})
        )
        return format_html('<a href="{}">{}</a>', url, obj.user_id)

    posts_count.short_description = "Posts"
    comments_count.short_description = "Comments"
    following_count.short_description = "Following"
    followers_count.short_description = "Followers"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("body", "user_link", "post_link", "date", "active", )
    search_fields = ("body__icontains", "user__user__username") 
    list_filter = ("date", "active", )
    actions = (make_comments_inactive, )

    def user_link(self, obj):
        url = (
            reverse("admin:api_account_change", kwargs={'object_id':obj.user.user.id})
        )
        return format_html('<a href="{}">{}</a>', url, obj.user.user.username)

    def post_link(self, obj):
        url = (
            reverse("admin:api_post_change", kwargs={'object_id':obj.post.id})
        )
        return format_html('<a href="{}">{}</a>', url, obj.post)


