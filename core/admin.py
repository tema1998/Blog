from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin for Post model.
    """
    list_display = ('id', 'user_profile', 'get_html_image', 'comments_status', 'created_at')
    list_display_links = ('id', 'get_html_image', 'created_at')
    search_fields = ('id', 'caption')
    list_editable = ('comments_status',)
    list_filter = ('created_at',)
    fieldsets = (
        ('Post settings',
         {'fields': ('id','user_profile', 'comments_status')}
         ),
        ('Post data',
         {'fields': ('image', 'caption'),
          'description': 'You are able to moderate this fields.'}
         ),
        ('Post info',
         {'fields': ('no_of_likes', 'created_at')}
         ),
    )
    readonly_fields = ('created_at', 'no_of_likes', 'user_profile')

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50 height=50>")

    get_html_image.short_description = 'Image'


class PostCommentsAdmin(admin.ModelAdmin):
    """
    Admin for PostComments model.
    """
    list_display = ('id', 'user_profile', 'post', 'date')
    list_display_links = ('id', 'post', 'date')
    search_fields = ('id', 'text', 'user')
    list_filter = ('date',)
    fields = ('id', 'user_profile', 'post', 'text', 'no_of_likes', 'date')
    readonly_fields = ('date', 'id', 'user_profile', 'post', 'no_of_likes')


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for Profile model.
    """
    list_display = ('id', 'user', 'get_html_image')
    list_display_links = ('id', 'user', 'get_html_image')
    search_fields = ('id', 'user')
    fieldsets = (
        ('Profile info',
         {'fields': ('id', 'user')}
         ),
        ('Profile data',
         {'fields': ('profile_img', 'bio', 'location'),
          'description': 'You are able to moderate this fields.'}
         ),
        ('User following settings',
         {'fields': ('following',)}
         ),
    )
    readonly_fields = ('id', 'user', )

    def get_html_image(self, object):
        if object.profile_img:
            return mark_safe(f"<img src='{object.profile_img.url}' width=50 height=50>")

    get_html_image.short_description = 'Image'


class PostLikesAdmin(admin.ModelAdmin):
    """
    Admin for PostLikes model.
    """
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('id', 'user', 'post')


class CommentLikesAdmin(admin.ModelAdmin):
    """
    Admin for CommentLikes model.
    """
    list_display = ('id', 'user', 'comment')
    list_display_links = ('id', 'user', 'comment')
    search_fields = ('id', 'user', 'comment')


class UserFavouritePostsAdmin(admin.ModelAdmin):
    """
    Admin for UserFavouritePosts model.
    """
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('id', 'user', 'post')


admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PostLikes, PostLikesAdmin)
admin.site.register(CommentLikes, CommentLikesAdmin)
admin.site.register(UserFavoritePosts, UserFavouritePostsAdmin)
