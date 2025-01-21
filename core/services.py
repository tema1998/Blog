from typing import Any
from uuid import UUID

from django.db.models import Q, QuerySet
from users.models import User

from .models import (
    CommentLikes,
    Post,
    PostComments,
    PostLikes,
    Profile,
    UserFavoritePosts,
)


class UserService:
    @staticmethod
    def get_user(username: str) -> QuerySet[User]:
        """
        Return user object by username.
        """
        return User.objects.get(username=username)

    @staticmethod
    def get_user_profile(user_id: int) -> QuerySet[Profile]:
        """
        Return user profile object by user ID.
        """
        return Profile.objects.get(user_id=user_id)

    @staticmethod
    def get_user_friends_suggestions(
        current_user_profile: Profile,
    ) -> QuerySet[Profile]:
        """`
        Return profiles who followed to user and user is not followed to theirs.
        """
        people_who_user_followed = UserService.get_people_who_user_followed(
            current_user_profile
        )
        people_who_user_followed_id = [
            obj.id for obj in people_who_user_followed
        ]
        people_who_user_followed_id.append(current_user_profile.id)
        return (
            Profile.objects.exclude(id__in=people_who_user_followed_id)
            .select_related("user")
            .only("bio", "profile_img", "user__username")
            .all()
            .order_by("?")[:5]
        )

    @staticmethod
    def get_people_who_user_followed(
        userprofile: Profile,
    ) -> QuerySet[Profile]:
        """
        Return profiles who followed to user.
        """
        return userprofile.following.all()


class PostService:
    @staticmethod
    def get_posts_of_friends(user_id: int) -> QuerySet[Post]:
        """
        Return user's friends' posts sorted by created date.
        """
        user_profile = UserService.get_user_profile(user_id)
        list_of_subscriptions = user_profile.following.values_list(
            "id", flat=True
        )

        return (
            Post.objects.select_related("user", "user_profile")
            .prefetch_related(
                "postcomments_set",
                "postcomments_set__user",
                "postcomments_set__user_profile",
            )
            .only(
                "user__username",
                "user__id",
                "user_profile__profile_img",
                "id",
                "image",
                "caption",
                "created_at",
                "no_of_likes",
                "comments_status",
            )
            .filter(
                Q(user__id__in=list_of_subscriptions) | Q(user__id=user_id)
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_post(post_id: UUID) -> QuerySet[Post]:
        """
        Return post object by ID.
        """
        return Post.objects.get(id=post_id)

    @staticmethod
    def create_new_post(
        user: User, user_profile: Profile, image, caption
    ) -> QuerySet[Post]:
        """
        Create post object.
        """
        return Post.objects.create(
            user=user, user_profile=user_profile, image=image, caption=caption
        )

    @staticmethod
    def get_like_post_obj(post, user) -> QuerySet[PostLikes]:
        """
        Return post's likes object.
        """
        return PostLikes.objects.get(post=post, user=user)

    @staticmethod
    def create_like_post_obj(post, user) -> QuerySet[PostLikes]:
        """
        Create like to post and
        return post's like object.
        """
        return PostLikes.objects.create(post=post, user=user)

    @staticmethod
    def get_user_posts_select_and_prefetch(user) -> QuerySet[Post]:
        """
        Return user's posts sorted by created date.
        """
        user_posts = (
            Post.objects.select_related("user", "user_profile")
            .prefetch_related(
                "postcomments_set",
                "postcomments_set__user",
                "postcomments_set__user_profile",
            )
            .only(
                "user__username",
                "user__id",
                "user_profile__profile_img",
                "id",
                "image",
                "caption",
                "created_at",
                "no_of_likes",
                "comments_status",
            )
            .filter(user=user)
            .order_by("-created_at")
        )
        return user_posts


class FavoritePostService:
    @staticmethod
    def get_favorite_post(
        post: Post, user: User
    ) -> QuerySet[UserFavoritePosts]:
        """
        Return user's favourite post object.
        """
        return UserFavoritePosts.objects.get(post=post, user=user)

    @staticmethod
    def create_favorite_post(
        user: User, post: Post
    ) -> QuerySet[UserFavoritePosts]:
        """
        Create a user favorite post object.
        """
        return UserFavoritePosts.objects.create(user=user, post=post)

    @staticmethod
    def delete_favorite_post(user_favourite_post: UserFavoritePosts) -> None:
        """
        Delete user's favourite post object.
        """
        user_favourite_post.delete()

    @staticmethod
    def get_user_favorite_posts(user: User) -> QuerySet[Post]:
        """
        Return user's favourite posts.
        """
        user_favorite_posts_ids = (
            UserFavoritePosts.objects.select_related("post")
            .filter(user=user)
            .values_list("post__id", flat=True)
        )

        return (
            Post.objects.select_related("user", "user_profile")
            .prefetch_related(
                "postcomments_set",
                "postcomments_set__user",
                "postcomments_set__user_profile",
            )
            .only(
                "user__username",
                "user__id",
                "user_profile__profile_img",
                "id",
                "image",
                "caption",
                "created_at",
                "no_of_likes",
                "comments_status",
            )
            .filter(id__in=user_favorite_posts_ids)
        )


class CommentService:
    @staticmethod
    def get_comment(comment_id: int) -> QuerySet[PostComments]:
        """
        Return comments to post.
        """
        return PostComments.objects.get(id=comment_id)

    @staticmethod
    def like_comment(comment: PostComments, user: User) -> None:
        """
        Create like for comment.
        """
        CommentLikes.objects.create(comment=comment, user=user)
        comment.no_of_likes += 1
        comment.save()

    @staticmethod
    def dislike_comment(
        comment: PostComments, comment_like: CommentLikes
    ) -> None:
        """
        Dislike a comment.
        """
        comment_like.delete()
        comment.no_of_likes -= 1
        comment.save()

    @staticmethod
    def get_comment_like(
        comment: PostComments, user: User
    ) -> QuerySet[CommentLikes]:
        """
        Return user's like to comment.
        For checking if post liked or not.
        """
        return CommentLikes.objects.filter(comment=comment, user=user).first()


class ProfileService:
    @staticmethod
    def get_all_user_profiles() -> QuerySet[Profile]:
        """
        Return all profiles.
        """
        return Profile.objects.select_related("user").all()

    @staticmethod
    def get_all_user_profile_followers(
        user_profile: Profile,
    ) -> QuerySet[Profile]:
        """
        Return user profiles that are followed by the user.
        """
        return user_profile.followers.all()

    @staticmethod
    def get_all_user_profile_following(
        user_profile: Profile,
    ) -> QuerySet[Profile]:
        """
        Return user profiles that the user is following.
        """
        return user_profile.following.all()

    @staticmethod
    def filter_user_profiles_by_username(username: str) -> QuerySet[Profile]:
        """
        Return profiles which contains username.
        """
        return (
            Profile.objects.select_related("user")
            .filter(user__username__contains=username)
            .only(
                "user__username", "user__id", "bio", "profile_img", "location"
            )
        )


class CommentStatusService:
    @staticmethod
    def check_post_comments_status(post: Post) -> Any:
        """
        Check if comments for post are disabled.
        Return bool.
        """
        return post.comments_status

    @staticmethod
    def disable_post_comments(post: Post) -> None:
        """
        Disable post's comments.
        """
        post.comments_status = False
        post.save()

    @staticmethod
    def enable_post_comments(post: Post) -> None:
        """
        Enable post's comments.
        """
        post.comments_status = True
        post.save()


class QuerySetService:
    @staticmethod
    def count_queryset(queryset) -> Any:
        """
        Return amount of queryset entries.
        """
        return queryset.count()
