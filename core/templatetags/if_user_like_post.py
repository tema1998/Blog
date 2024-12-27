from core.models import PostLikes
from django import template
from django.contrib.auth import get_user_model


register = template.Library()
User = get_user_model()


@register.simple_tag(takes_context=True)
def if_user_like_post(context, post_id):
    request = context["request"]
    try:
        PostLikes.objects.get(user=request.user.id, post__id=post_id)
        like_status = True
    except Exception:
        like_status = False
    return like_status
