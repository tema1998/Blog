from django.contrib import admin
from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts

admin.site.register(PostComments)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(CommentLikes)
admin.site.register(UserFavoritePosts)
