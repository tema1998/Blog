from django import template

from core.models import Profile, Post, UserFavoritePosts

register = template.Library()


@register.simple_tag(takes_context=True)
def if_user_add_post_to_favorites(context, post_id):
    request = context['request']

    try:
        user_favorites_obj = UserFavoritePosts.objects.get(user=request.user.id, post__id=post_id)
        favorite_button = 'Remove from favorites'
    except:
        favorite_button = 'Add to favorites'

    return favorite_button