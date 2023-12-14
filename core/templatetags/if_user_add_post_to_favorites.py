from django import template

from core.models import Profile, Post, UserFavoritePosts

register = template.Library()


@register.simple_tag()
def if_user_add_post_to_favorites(post_id, user_id):

    try:
        current_user_profile = Profile.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        user_favorites_obj = UserFavoritePosts.objects.get(user_profile=current_user_profile)
        user_favorites_posts = user_favorites_obj.posts.all()
        if post in user_favorites_posts:
            return True
        else:
            return False
    except:
        return False