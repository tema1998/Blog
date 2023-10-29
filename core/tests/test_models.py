from django.test import TestCase
from datetime import datetime
from django.contrib.auth.models import User
from core.models import Profile, Post


# class ProfileModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
#         user.save()
#         Profile.objects.create(user=user, id_user=user.id, bio='I like going for a walk', location='Minsk')
#
#     def setUp(self):
#         pass
#
#     def test_bio_label(self):
#         profile = Profile.objects.get(id=1)
#         field_label = profile._meta.get_field('bio').verbose_name
#         self.assertEquals(field_label, 'Information')
#
#     def test_profileimg_label(self):
#         profile = Profile.objects.get(id=1)
#         field_label = profile._meta.get_field('profileimg').verbose_name
#         self.assertEquals(field_label, 'profileimg')
#
#     def test_location_label(self):
#         profile = Profile.objects.get(id=1)
#         field_label = profile._meta.get_field('location').verbose_name
#         self.assertEquals(field_label, 'location')
#
#     def test_bio_max_length(self):
#         profile = Profile.objects.get(id=1)
#         max_length = profile._meta.get_field('bio').max_length
#         self.assertEquals(max_length, 300)
#
#     def test_location_max_length(self):
#         profile = Profile.objects.get(id=1)
#         max_length = profile._meta.get_field('location').max_length
#         self.assertEquals(max_length, 100)
#
#     def test_object_name_is_username(self):
#         profile = Profile.objects.get(id=1)
#         expected_object_name = profile.user.username
#         self.assertEquals(expected_object_name, str(profile))
#
#     def test_get_absolute_url(self):
#         profile = Profile.objects.get(id=1)
#         # This will also fail if the urlconf is not defined.
#         self.assertEquals(profile.get_absolute_url(), '/profile/username/')


# class PostModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
#         user.save()
#         user = User.objects.get(id=1)
#         user_id = user.id
#         Post.objects.create(id=user.id, user=user, caption='caption')
#
#     def setUp(self):
#         pass
#
#     def test_id_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field('id').verbose_name
#         self.assertEquals(field_label, 'id')
#
#     def test_user_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field('user').verbose_name
#         self.assertEquals(field_label, 'user')
#
#     def test_image_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field('image').verbose_name
#         self.assertEquals(field_label, 'image')
#
#     def test_caption_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field('caption').verbose_name
#         self.assertEquals(field_label, 'caption')
#
#     # def test_image_label(self):
#     #     post = Post.objects.get(id=1)
#     #     field_label = post._meta.get_field('created_at').verbose_name
#     #     self.assertEquals(field_label, 'created at1')
#     #     print('----------------------------')
#     #     print(field_label)
#
#     def test_no_of_likes_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field('no_of_likes').verbose_name
#         self.assertEquals(field_label, 'no of likes')
#
#     def test_caption_length(self):
#         post = Post.objects.get(id=1)
#         max_length = post._meta.get_field('caption').max_length
#         self.assertEquals(max_length, 1000)
#
#     def test_object_name_is_username(self):
#         post = Post.objects.get(id=1)
#         expected_object_name = post.user
#         self.assertEquals(expected_object_name, str(post))
#
#     # def test_get_comment(self):
#     #     post=Post.objects.get(id=1)
#     #     #This will also fail if the urlconf is not defined.
#     #     self.assertEquals(post.get_absolute_url(),'/profile/username/')
