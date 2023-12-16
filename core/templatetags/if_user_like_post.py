from django import template
from django.contrib.auth import get_user_model
from core.models import Post, PostLikes

register = template.Library()
User = get_user_model()


@register.simple_tag(takes_context=True)
def if_user_like_post(context, post_id):
    request = context['request']
    try:
        is_user_liked = PostLikes.objects.get(user=request.user.id, post__id=post_id)
        like_status = True
    except:
        like_status = False
    return like_status
