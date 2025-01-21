from core.models import Profile
from core.services import UserService
from django import template


register = template.Library()


@register.inclusion_tag("core/include/sidebar_users.html")
def user_friends_suggestions(user_id):
    """
    Inclusion tag for render friends suggestion block.
    """
    current_user_profile = Profile.objects.get(id=user_id)
    user_friends_suggestion = UserService.get_user_friends_suggestions(
        current_user_profile
    )
    return {"user_friends_suggestions": user_friends_suggestion}
