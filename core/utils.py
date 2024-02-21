from .models import *
from users.models import User


class GetUserProfileInContext:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_object = User.objects.get(username=self.request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        context['current_user_profile'] = user_profile
        return context