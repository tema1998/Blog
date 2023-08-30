from itertools import chain

from django.contrib.auth.models import User, auth
from .models import Profile, Post, LikePost, Commentss, LikeComments, Chat, Message


def get_current_user(request):
    return request.user


def get_user_profile_by_username(username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    return user_profile


def get_people_who_user_followed_by_userprofile(userprofile):
    people_who_user_followed = userprofile.following.all()
    return people_who_user_followed


def get_people_who_are_followed_user_by_userprofile(userprofile):
    people_who_are_followed_user = userprofile.followers.all()
    return people_who_are_followed_user


def get_user_friends_feeds_list_by_userprofile(userprofile):
    user_following_list = []
    user_friends_feeds = []

    people_who_user_followed = get_people_who_user_followed_by_userprofile(userprofile)

    for person in people_who_user_followed:
        person_feeds_lists = Post.objects.filter(user=person)
        user_friends_feeds.append(person_feeds_lists)

    # Adding personal feeds of user
    user_friends_feeds.append(Post.objects.filter(user=username))
    unpacked_user_feeds_list = list(chain(*user_friends_feeds))
    return unpacked_user_feeds_list


def get_user_friends_suggestions(request):
    current_user_profile = get_user_profile_by_username(get_current_user(request).username)

    all_users = User.objects.all()

    # 1)Первая часть те, кто подписался на юзера, но юзер не подписался на них
    # 2)Вторая часть те кто друзья друзей
    # Если не хватает друзей друзей, то берем рандомно тех на кого не подписан юзер

    # Получим список тех на кого вообще подписан юзер:
    people_who_user_followed = get_people_who_user_followed_by_userprofile(current_user_profile)

    # Получим список тех кто подписан на юзера:
    people_who_are_followed_user = get_people_who_are_followed_user_by_userprofile(current_user_profile)

    # 1)Получим список тех кто подписан на юзера, но юзер на них не подписан
    people_who_are_followed_user_but_user_havent_followed_theirs = [person for person in people_who_are_followed_user if
                                                                 person not in people_who_user_followed]
    print(people_who_are_followed_user_but_user_havent_followed_theirs)
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
