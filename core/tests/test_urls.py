from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import *


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func.view_class, Index)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, Signup)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func.view_class, Signin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, Logout)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEqual(resolve(url).func.view_class, Settings)

    def test_upload_url_resolves(self):
        url = reverse('add-post')
        self.assertEqual(resolve(url).func.view_class, AddPost)

    def test_follow_url_resolves(self):
        url = reverse('follow', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProfileFollowingCreateView)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['some-args'])
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_edit_post_url_resolves(self):
        url = reverse('edit-post', args=['some-args'])
        self.assertEqual(resolve(url).func.view_class, EditPost)

    def test_like_post_url_resolves(self):
        url = reverse('like-post', args=['213-324'])
        self.assertEqual(resolve(url).func.view_class, LikePost)

    def test_delete_post_url_resolves(self):
        url = reverse('delete-post')
        self.assertEqual(resolve(url).func.view_class, DeletePost)

    def test_disable_post_comments_url_resolves(self):
        url = reverse('disable-post-comments')
        self.assertEqual(resolve(url).func.view_class, DisablePostComments)

    def test_enable_post_comments_url_resolves(self):
        url = reverse('enable-post-comments')
        self.assertEqual(resolve(url).func.view_class, EnablePostComments)

    def test_add_comment_url_resolves(self):
        url = reverse('add-comment')
        self.assertEqual(resolve(url).func.view_class, AddComment)

    def test_like_comment_url_resolves(self):
        url = reverse('like-comment', args=[2213])
        self.assertEqual(resolve(url).func.view_class, LikeComment)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, Search)