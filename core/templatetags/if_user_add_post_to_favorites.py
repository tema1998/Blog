from core.models import UserFavoritePosts
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def if_user_add_post_to_favorites(context, post_id):
    """
    Simple tag for to find out is user add post to favorites and generate button text.
    """
    request = context["request"]

    try:
        UserFavoritePosts.objects.get(user=request.user.id, post__id=post_id)
        favorite_button = "Remove from favorites"
    except Exception:
        favorite_button = "Add to favorites"

    return favorite_button
