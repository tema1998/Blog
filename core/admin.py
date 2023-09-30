from django.contrib import admin
from .models import Profile, Post, PostLikes, PostComments, CommentLikes, Chat, Message

admin.site.register(PostComments)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(CommentLikes)
admin.site.register(Chat)
admin.site.register(Message)