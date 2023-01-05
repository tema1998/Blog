from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Commentss, LikeComments, Chat, Message

admin.site.register(Commentss)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(LikeComments)
admin.site.register(Chat)
admin.site.register(Message)