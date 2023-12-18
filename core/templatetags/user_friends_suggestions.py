from django import template

from core.models import Profile
from core.services import get_user_friends_suggestions

register = template.Library()


@register.inclusion_tag('core/include/sidebar_users.html')
def user_friends_suggestions(user_id):
    current_user_profile = Profile.objects.get(id=user_id)
    user_friends_suggestion = get_user_friends_suggestions(current_user_profile)
    return {'user_friends_suggestions': user_friends_suggestion}