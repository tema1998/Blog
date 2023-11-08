from itertools import chain

from django.contrib.auth.models import User, auth
from django.http import Http404

from .models import Profile, Post, PostLikes, PostComments, CommentLikes, Chat, Message


def check_if_comment_disable(post):
    return post.disable_comments


def get_post_by_id(post_id):
    return Post.objects.select_related('user').get(id=post_id)


def get_current_user(request):
    return request.user

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


def get_people_who_are_followed_user_by_userprofile(userprofile):
    people_who_are_followed_user = userprofile.followers.select_related('user').only('bio', 'profileimg',
                                                                                     'user__username').all()
    return people_who_are_followed_user


def get_user_friends_suggestions(current_user_profile):

    # 1)Первая часть те, кто подписался на юзера, но юзер не подписался на них
    # 2)Вторая часть те кто друзья друзей
    # Если не хватает друзей друзей, то берем рандомно тех на кого не подписан юзер

    # Получим список тех на кого вообще подписан юзер:
    people_who_user_followed = get_people_who_user_followed_by_userprofile(current_user_profile)


    # Получим список тех кто подписан на юзера:
    people_who_are_followed_user = get_people_who_are_followed_user_by_userprofile(current_user_profile)

    # 1)Получим список тех кто подписан на юзера, но юзер на них не подписан
    people_who_are_followed_user_but_user_havent_followed_theirs = [user_profile for user_profile in
                                                                    people_who_are_followed_user if user_profile not in
                                                                    people_who_user_followed]
    # their_profiles = [Profile.objects.get(user_id=person.id) for person in
    #                   people_who_are_followed_user_but_user_didnt_follow_theirs]

    return people_who_are_followed_user_but_user_havent_followed_theirs
    # for user in user_following:
    #         user_list = User.objects.get(username=username)
    #         user_following_all.append(user_list)
    #
    #     new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    #     current_user = User.objects.filter(username=request.user.username)
    #     final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    #     random.shuffle(final_suggestions_list)
    #     username_profile = []
    #     username_profile_list = []
    #
    #     for users in final_suggestions_list:
    #         username_profile.append(users.id)
    #
    #     for id in username_profile:
    #         profile_list = Profile.objects.filter(user_id=id)
    #         username_profile_list.append(profile_list)
    #
    #     suggestions_username_profile_list = list(chain(*username_profile_list))


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
