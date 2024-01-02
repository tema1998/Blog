from django.contrib.auth.models import User, auth
from django.db.models import Q

from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts


def get_user(username: str):
    return User.objects.get(username=username)


def get_user_profile(user_id: int):
    return Profile.objects.get(user_id=user_id)


def get_posts_of_friends(user_id: int):
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


def get_post(id: int):
    return Post.objects.get(id=id)


def get_like_post_obj(post, user):
    return PostLikes.objects.get(post=post, user=user)


def create_like_post_obj(post, user):
    return PostLikes.objects.create(post=post, user=user)


def get_favorite_post(post, user):
    return UserFavoritePosts.objects.get(post=post, user=user)


def create_favorite_post(user, post):
    UserFavoritePosts.objects.create(user=user, post=post)


def delete_favorite_post(user_favourite_post):
    user_favourite_post.delete()


def create_user_profile(user):
    return Profile.objects.create(user=user)


def check_if_post_comment_disable(post):
    return post.disable_comments


def get_all_user_profile_followers(user_profile):
    return user_profile.followers.all()


def get_all_user_profile_following(user_profile):
    return user_profile.following.all()


def get_all_user_profiles():
    return Profile.objects.select_related('user').all()


def get_user_posts_select_and_prefetch(user):
    user_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                      'postcomments_set__user',
                                                                                      'postcomments_set__user_profile', ) \
        .only('user__username', 'user__id', 'user_profile__profileimg', 'id', 'image', 'caption', 'created_at',
              'no_of_likes',
              'disable_comments').filter(user=user).order_by('-created_at')
    return user_posts


def count_queryset(queryset):
    return queryset.count()


def filter_user_profiles_by_username(username):
    search_users_profile_list = Profile.objects.select_related('user') \
        .filter(user__username__contains=username).only('user__username', 'user__id', 'bio', 'profileimg',
                                                        'location')
    return search_users_profile_list


def get_comment(comment_id):
    return PostComments.objects.get(id=comment_id)


def like_comment(comment, user):
    CommentLikes.objects.create(comment=comment, user=user)
    comment.no_of_likes += 1
    comment.save()


def dislike_comment(comment, comment_like):
    comment_like.delete()
    comment.no_of_likes -= 1
    comment.save()


def get_comment_like(comment, user):
    return CommentLikes.objects.filter(comment=comment, user=user).first()


def get_people_who_user_followed_by_userprofile(userprofile):
    people_who_user_followed = userprofile.following.all()
    return people_who_user_followed


def get_user_friends_suggestions(current_user_profile):
    people_who_user_followed = get_people_who_user_followed_by_userprofile(current_user_profile)
    people_who_user_followed_id = [obj.id for obj in people_who_user_followed]
    people_who_user_followed_id.append(current_user_profile.id)
    people_who_are_followed_user_but_user_havent_followed_theirs = Profile.objects.exclude(
        id__in=people_who_user_followed_id).select_related('user') \
                                                                       .only('bio', 'profileimg',
                                                                             'user__username').all().order_by('?')[:5]

    return people_who_are_followed_user_but_user_havent_followed_theirs


def disable_post_comments(post):
    post.disable_comments = True
    post.save()


def enable_post_comments(post):
    post.disable_comments = False
    post.save()


def get_user_favorite_posts(user) -> list:
    user_favorite = UserFavoritePosts.objects.filter(user=user)
    user_favorite_posts = [obj.post for obj in list(user_favorite)]
    return user_favorite_posts


def create_new_post(user, user_profile, image, caption, disable_comments):
    Post.objects.create(user=user, user_profile=user_profile, image=image, caption=caption,
                        disable_comments=disable_comments)