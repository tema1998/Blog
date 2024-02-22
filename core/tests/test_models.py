from django.test import TestCase
from datetime import datetime
from users.models import User

from core.models import *


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')

    def setUp(self):
        pass

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_bio_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'Information')

    def test_profileimg_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('profileimg').verbose_name
        self.assertEquals(field_label, 'Profile image')

    def test_location_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('location').verbose_name
        self.assertEquals(field_label, 'Location')

    def test_following_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('following').verbose_name
        self.assertEquals(field_label, 'Subscriptions')

    def test_bio_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, 300)

    def test_location_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('location').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_username(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = profile.user.username
        self.assertEquals(expected_object_name, str(profile))

    def test_get_absolute_url(self):
        profile = Profile.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(profile.get_absolute_url(), '/profile/username/')


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        user_profile = Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')
        user = User.objects.get(id=1)
        post_object = Post.objects.create(user=user, user_profile=user_profile, caption='caption')

    def setUp(self):
        pass

    def test_id_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('id').verbose_name
        self.assertEquals(field_label, 'Post ID')

    def test_user_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_user_profile_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('user_profile').verbose_name
        self.assertEquals(field_label, 'User profile')

    def test_image_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Post image')

    def test_caption_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('caption').verbose_name
        self.assertEquals(field_label, 'Caption')

    def test_created_at_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')

    def test_no_of_likes_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('no_of_likes').verbose_name
        self.assertEquals(field_label, 'Number of likes')

    def test_comments_status_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field('comments_status').verbose_name
        self.assertEquals(field_label, 'Disabled comments')

    def test_caption_length(self):
        post = Post.objects.first()
        max_length = post._meta.get_field('caption').max_length
        self.assertEquals(max_length, 1000)

    def test_str(self):
        post = Post.objects.first()
        expected_object_name = f'ID: {post.id}'
        self.assertEquals(expected_object_name, str(post))

    def test_get_author_photo(self):
        post = Post.objects.first()
        self.assertEquals(post.get_author_photo(),'/media/blank_profile.png')


class UserFavoritePostsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        user_profile = Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')
        user = User.objects.get(id=1)
        post = Post.objects.create(user=user, user_profile=user_profile, caption='caption')
        user_favorite = UserFavoritePosts.objects. create(user=user, post=post)

    def test_user_label(self):
        user_favorite = UserFavoritePosts.objects.first()
        field_label = user_favorite._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_post_label(self):
        user_favorite = UserFavoritePosts.objects.first()
        field_label = user_favorite._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Post')


class PostLikesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        user_profile = Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')
        user = User.objects.get(id=1)
        post = Post.objects.create(user=user, user_profile=user_profile, caption='caption')
        post_like = PostLikes.objects. create(user=user, post=post)

    def test_user_label(self):
        post_like = PostLikes.objects.first()
        field_label = post_like._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_post_label(self):
        post_like = PostLikes.objects.first()
        field_label = post_like._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Post')

    def test_str(self):
        post_like = PostLikes.objects.first()
        expected_object_name = f'{post_like.user} likes {post_like.post}'
        self.assertEquals(expected_object_name, str(post_like))


class PostCommentsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        user_profile = Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')
        user = User.objects.get(id=1)
        post = Post.objects.create(user=user, user_profile=user_profile, caption='caption')
        post_comment = PostComments.objects.create(user=user, user_profile=user_profile, text='text123', post=post)

    def setUp(self):
        pass

    def test_user_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_user_profile_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('user_profile').verbose_name
        self.assertEquals(field_label, 'User profile')

    def test_image_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Comment text')

    def test_caption_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Post')

    def test_created_at_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('no_of_likes').verbose_name
        self.assertEquals(field_label, 'Comment likes')

    def test_no_of_likes_label(self):
        post_comment = PostComments.objects.first()
        field_label = post_comment._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'Date of creation')

    def test_text_length(self):
        post_comment = PostComments.objects.first()
        max_length = post_comment._meta.get_field('text').max_length
        self.assertEquals(max_length, 1000)

    def test_str(self):
        post_comment = PostComments.objects.first()
        expected_object_name = f'Comment by {post_comment.user} - {post_comment.date}'
        self.assertEquals(expected_object_name, str(post_comment))

    def test_user_photo(self):
        post_comment = PostComments.objects.first()
        self.assertEquals(post_comment.user_photo(), '/media/blank_profile.png')


class CommentLikesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        user_profile = Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')
        user = User.objects.get(id=1)
        post = Post.objects.create(user=user, user_profile=user_profile, caption='caption')
        comment = PostComments.objects.create(user=user, user_profile=user_profile, text='text123', post=post)
        comment_like = CommentLikes.objects. create(user=user, comment=comment)

    def test_user_label(self):
        comment_like = CommentLikes.objects.first()
        field_label = comment_like._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_post_label(self):
        comment_like = CommentLikes.objects.first()
        field_label = comment_like._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'Comment')

    def test_str(self):
        comment_like = CommentLikes.objects.first()
        expected_object_name = f'{comment_like.pk}'
        self.assertEquals(expected_object_name, str(comment_like))
