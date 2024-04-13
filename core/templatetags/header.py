from django import template

from core.models import Profile
from core.services import get_user_friends_suggestions

register = template.Library()


@register.inclusion_tag('core/include/header.html', takes_context=True)
def header(context):
    request = context['request']
    current_user_profile = Profile.objects.get(user_id=request.user.id)
    current_user_profile_img_url = current_user_profile.profile_img.url
    current_user_profile_url = current_user_profile.get_absolute_url
    return {'current_user_profile_img_url': current_user_profile_img_url,
            'current_user_profile_url': current_user_profile_url}