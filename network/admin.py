from django.contrib import admin

from .models import User, Post, Like, Follower

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'post_content', 'post_time')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'liker_id', 'post_id')

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'follow_initiator', 'follow_reciever')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(User, UserAdmin)
