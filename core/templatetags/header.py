from core.models import Profile
from django import template


register = template.Library()


@register.inclusion_tag("core/include/header.html", takes_context=True)
def header(context):
    """
    Inclusion tag for render header with user's profile's data.
    """
    request = context["request"]
    current_user_profile = Profile.objects.get(user_id=request.user.id)
    current_user_profile_img_url = current_user_profile.profile_img.url
    current_user_profile_url = current_user_profile.get_absolute_url
    return {
        "current_user_profile_img_url": current_user_profile_img_url,
        "current_user_profile_url": current_user_profile_url,
    }
