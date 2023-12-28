from itertools import chain

from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http import Http404

from .models import Profile, Post, PostLikes, PostComments, CommentLikes


def get_user_profile(user_id: int):
    return Profile.objects.get(user_id=user_id)


def get_friends_posts(user_id: int):
    user_profile = get_user_profile(user_id=user_id)
    list_of_subscriptions = user_profile.following.values_list('id', flat=True)
    list_of_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                         'postcomments_set__user',
                                                                                         'postcomments_set__user_profile',
                                                                                         ) \
        .only('user__username', 'user__id', 'user_profile__profileimg', 'id', 'image', 'caption', 'created_at',
              'no_of_likes',
              'disable_comments').filter(
        Q(user__id__in=list_of_subscriptions) | Q(user__id__in=[user_id])).order_by('-created_at')

    return list_of_posts


#Было select related User, требуется ли?
def get_post(id: int):
    return Post.objects.get(id=id)


def check_if_comment_disable(post):
    return post.disable_comments


def get_user_profile_by_user_object(user_object):
    user_profile = Profile.objects.select_related('user').get(user=user_object)
    return user_profile


def get_user_profile_by_username(username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    return user_profile


def get_people_who_user_followed_by_userprofile(userprofile):
    people_who_user_followed = userprofile.following.all()
    return people_who_user_followed


def get_user_friends_suggestions(current_user_profile):

    people_who_user_followed = get_people_who_user_followed_by_userprofile(current_user_profile)
    people_who_user_followed_id = [obj.id for obj in people_who_user_followed]
    people_who_user_followed_id.append(current_user_profile.id)
    people_who_are_followed_user_but_user_havent_followed_theirs = Profile.objects.exclude(id__in=people_who_user_followed_id).select_related('user') \
                                                                       .only('bio', 'profileimg',
                                                                             'user__username').all().order_by('?')[:5]

    return people_who_are_followed_user_but_user_havent_followed_theirs


def disable_comments(post):
    post.disable_comments = True
    post.save()


def enable_comments(post):
    post.disable_comments = False
    post.save()


def get_user_id_for_get_and_post_methods(request):
    try:
        if request.method == 'GET':
            user_id = request.user.id
        else:
            user_id = int(request.POST['user_id'])
        return user_id
    except Exception:
        raise Http404


def if_user_is_post_owner(post, user):
    user_id = user.id
    post_author_id = post.user.id
    return user_id == post_author_id


def if_user_is_authenticated(request):
    return request.user.is_authenticated
