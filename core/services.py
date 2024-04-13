from django.db.models import Q, QuerySet

from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts
from users.models import User


def get_user(username: str):
    """
    Return user object.
    """
    return User.objects.get(username=username)


def get_user_profile(user_id):
    """
    Return user profile object.
    """
    return Profile.objects.get(user_id=user_id)


def get_posts_of_friends(user_id):
    """
    Return user's friends' posts sorted by created date.
    """
    user_profile = get_user_profile(user_id=user_id)
    list_of_subscriptions = user_profile.following.values_list('id', flat=True)
    list_of_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                         'postcomments_set__user',
                                                                                         'postcomments_set__user_profile',
                                                                                         ) \
        .only('user__username', 'user__id', 'user_profile__profile_img', 'id', 'image', 'caption', 'created_at',
              'no_of_likes',
              'comments_status').filter(
        Q(user__id__in=list_of_subscriptions) | Q(user__id__in=[user_id])).order_by('-created_at')

    return list_of_posts


def get_post(id):
    """
    Return post object.
    """
    return Post.objects.get(id=id)


def get_like_post_obj(post, user):
    """
    Return post's likes object.
    """
    return PostLikes.objects.get(post=post, user=user)


def create_like_post_obj(post, user):
    """
    Create like to post and
    return post's like object.
    """
    return PostLikes.objects.create(post=post, user=user)


def get_favorite_post(post, user):
    """
    Return user's favourite posts.
    """
    return UserFavoritePosts.objects.get(post=post, user=user)


def create_favorite_post(user, post):
    """
    Create user's favourite post object.
    """
    UserFavoritePosts.objects.create(user=user, post=post)


def delete_favorite_post(user_favourite_post):
    """
    Delete user's favourite post object.
    """
    user_favourite_post.delete()


def check_post_comments_status(post):
    """
    Check if comments to post are disabled.
    Return bool.
    """
    return post.comments_status


def get_all_user_profile_followers(user_profile):
    """
    Return users profiles who user followed.
    """
    return user_profile.followers.all()


def get_all_user_profile_following(user_profile):
    """
    Delete users profiles who followed to user.
    """
    return user_profile.following.all()


def get_all_user_profiles():
    """
    Return all profiles.
    """
    return Profile.objects.select_related('user').all()


def get_user_posts_select_and_prefetch(user):
    """
    Return user's posts sorted by created date.
    """
    user_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                      'postcomments_set__user',
                                                                                      'postcomments_set__user_profile',
                                                                                      ) \
        .only('user__username', 'user__id', 'user_profile__profile_img', 'id', 'image', 'caption', 'created_at',
              'no_of_likes',
              'comments_status').filter(user=user).order_by('-created_at')
    return user_posts


def count_queryset(queryset):
    """
    Return amount of queryset entries.
    """
    return queryset.count()


def filter_user_profiles_by_username(username):
    """
    Return profiles which contains username.
    """
    search_users_profile_list = Profile.objects.select_related('user') \
        .filter(user__username__contains=username).only('user__username', 'user__id', 'bio', 'profile_img',
                                                        'location')
    return search_users_profile_list


def get_comment(comment_id):
    """
    Return comments to post.
    """
    return PostComments.objects.get(id=comment_id)


def like_comment(comment, user):
    """
    Create like to comment
    """
    CommentLikes.objects.create(comment=comment, user=user)
    comment.no_of_likes += 1
    comment.save()


def dislike_comment(comment, comment_like):
    """
    Dislike to comment.
    """
    comment_like.delete()
    comment.no_of_likes -= 1
    comment.save()


def get_comment_like(comment, user):
    """
    Return user's like to comment.
    For checking if post liked or not.
    """
    return CommentLikes.objects.filter(comment=comment, user=user).first()


def get_people_who_user_followed_by_userprofile(userprofile):
    """
    Return profiles who followed to user.
    """
    people_who_user_followed = userprofile.following.all()
    return people_who_user_followed


def get_user_friends_suggestions(current_user_profile):
    """
    Return profiles who followed to user and
    user is not followed to theirs.
    """
    people_who_user_followed = get_people_who_user_followed_by_userprofile(current_user_profile)
    people_who_user_followed_id = [obj.id for obj in people_who_user_followed]
    people_who_user_followed_id.append(current_user_profile.id)
    people_who_are_followed_user_but_user_havent_followed_theirs = Profile.objects.exclude(
        id__in=people_who_user_followed_id).select_related('user') \
                                                                       .only('bio', 'profile_img',
                                                                             'user__username').all().order_by('?')[:5]

    return people_who_are_followed_user_but_user_havent_followed_theirs


def disable_post_comments(post):
    """
    Disable post's comments.
    """
    post.comments_status = False
    post.save()


def enable_post_comments(post):
    """
    Enable post's comments.
    """
    post.comments_status = True
    post.save()


def get_user_favorite_posts(user):
    """
    Return user's favourite posts.
    """
    user_favorite = UserFavoritePosts.objects.select_related('post').filter(user=user).only('post__id')
    user_favorite_posts_id = [obj.post.id for obj in list(user_favorite)]
    user_favorite_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                               'postcomments_set__user',
                                                                                               'postcomments_set__user_profile',
                                                                                               ) \
        .only('user__username', 'user__id', 'user_profile__profile_img', 'id', 'image', 'caption', 'created_at',
              'no_of_likes',
              'comments_status').filter(id__in=user_favorite_posts_id)
    return user_favorite_posts


def create_new_post(user, user_profile, image, caption):
    """
    Create post object.
    """
    Post.objects.create(user=user, user_profile=user_profile, image=image, caption=caption)
