from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'get_html_image', 'disable_comments', 'created_at')
    list_display_links = ('id', 'get_html_image', 'created_at')
    search_fields = ('id', 'caption')
    list_editable = ('disable_comments',)
    list_filter = ('created_at',)

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50 height=50>")

    get_html_image.short_description = 'Image'


class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'post', 'date')
    list_display_links = ('id', 'post', 'date')
    search_fields = ('id', 'text', 'user')
    list_filter = ('date',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_html_image')
    list_display_links = ('id', 'user', 'get_html_image')
    search_fields = ('id', 'user')

    def get_html_image(self, object):
        if object.profileimg:
            return mark_safe(f"<img src='{object.profileimg.url}' width=50 height=50>")

    get_html_image.short_description = 'Image'


class PostLikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('id', 'user', 'post')


class CommentLikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment')
    list_display_links = ('id', 'user', 'comment')
    search_fields = ('id', 'user', 'comment')


class UserFavouritePostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('id', 'user', 'post')


admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLikes, PostLikesAdmin)
admin.site.register(CommentLikes, CommentLikesAdmin)
admin.site.register(UserFavoritePosts, UserFavouritePostsAdmin)
