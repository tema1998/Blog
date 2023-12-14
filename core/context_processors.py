from .services import get_user_profile_by_username
from .forms import CommentForm
from .models import Profile, Post


# def get_current_user_profile(request):
#     if request.user.username:
#         current_user = request.user
#         current_user_profile = get_user_profile_by_username(current_user.username)
#         return {
#             'current_user': current_user,
#             'current_user_profile': current_user_profile,}
#     else:
#         return {
#             'current_user': None,
#             'current_user_profile': None, }

def get_current_user(request):
    form = CommentForm()
    return {
        'comment_form': form
    }
