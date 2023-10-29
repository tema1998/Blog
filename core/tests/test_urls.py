from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import *

class TestUrls(SimpleTestCase):

    # Resolve give us info about url, we get name func or class of View, and we compare class from view with class
    # from info.
    # Проверка что вызывается нужна вьюшка

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func.view_class, Index)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, Signup)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func.view_class, Signin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, Logout)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func.view_class, Settings)

    def test_upload_url_resolves(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func.view_class, Upload)

    def test_follow_url_resolves(self):
        url = reverse('follow', args=[1])
        self.assertEquals(resolve(url).func.view_class, ProfileFollowingCreateView)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['some-args'])
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_edit_post_url_resolves(self):
        url = reverse('edit-post', args=['some-args'])
        self.assertEquals(resolve(url).func.view_class, EditPost)

    def test_like_post_url_resolves(self):
        url = reverse('like-post')
        self.assertEquals(resolve(url).func.view_class, LikePost)

    def test_delete_post_url_resolves(self):
        url = reverse('delete-post')
        self.assertEquals(resolve(url).func.view_class, DeletePost)

    def test_disable_post_comments_url_resolves(self):
        url = reverse('disable-post-comments')
        self.assertEquals(resolve(url).func.view_class, DisablePostComments)

    def test_enable_post_comments_url_resolves(self):
        url = reverse('enable-post-comments')
        self.assertEquals(resolve(url).func.view_class, EnablePostComments)

    def test_add_comment_url_resolves(self):
        url = reverse('add-comment')
        self.assertEquals(resolve(url).func.view_class, AddComment)

    def test_like_comment_url_resolves(self):
        url = reverse('like-comment')
        self.assertEquals(resolve(url).func.view_class, Likecomment)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func.view_class, Search)

    def test_dialogs_url_resolves(self):
        url = reverse('dialogs')
        self.assertEquals(resolve(url).func.view_class, DialogsView)

    def test_create_dialog_url_resolves(self):
        url = reverse('create_dialog', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CreateDialogView)

    def test_messages_url_resolves(self):
        url = reverse('messages', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MessagesView)