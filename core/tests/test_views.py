from django.test import TestCase, Client
from django.urls import reverse, resolve
from core.models import *
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import AddPostForm

from io import BytesIO
from PIL import Image
from django.core.files.base import File

def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)

# class TestViews(TestCase):
#
#     def setUp(self):
#         #create user
#         self.user = User.objects.create_user(username='stasbasov')
#         #create profile
#         Profile.objects.create(user=self.user, profileimg='blank_profile.png', )
#         #auth
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#
#         self.index_url = reverse('index')
#         self.profile_view_url = reverse('profile', args=['stasbasov'])
#
#
#     def test_index_GET(self):
#         response = self.authorized_client.get(self.index_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'core/index.html')
#
#     def test_profile_GET(self):
#         response = self.authorized_client.get(self.profile_view_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'core/profile.html')
#
#
# class TaskPagesTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         datetime.datetime.now(tz=timezone.utc)
#
#     def setUp(self):
#         #time
#
#         # Создаем авторизованный клиент
#         self.user = User.objects.create_user(username='ivan')
#         self.client = Client()
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#
#         Profile.objects.create(user=self.user)
#
#         self.profile_view_url = reverse('profile', args=['ivan'])
#
#         self.post = Post.objects.create(user=self.user, image='blank_profile.png')
#
#         self.chat = Chat.objects.create()
#
#     # Проверяем используемые шаблоны
#     def test_auth_pages_uses_correct_template(self):
#
#         # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
#         templates_pages_names = {
#             'core/index.html': reverse('index'),
#             'core/edit_post.html': reverse('edit-post', kwargs={'post_id': self.post.id}),
#             'core/settings.html': reverse('settings'),
#             'core/profile.html': reverse('profile', kwargs={'username': 'ivan'}),
#             'core/dialogs.html': reverse('dialogs'),
#             'core/messages.html': reverse('messages', kwargs={'chat_id': self.chat.id}),
#         }
#         print(self.authorized_client.get(reverse('edit-post', kwargs={'post_id': self.post.id})))
#
#         # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
#         for template, reverse_name in templates_pages_names.items():
#             with self.subTest(reverse_name=reverse_name):
#                 response = self.authorized_client.get(reverse_name)
#                 self.assertTemplateUsed(response, template)
#
#     def test_pages_uses_correct_template(self):
#         """URL-адрес использует соответствующий шаблон."""
#         templates_pages_names = {
#             'core/signup.html': reverse('signup'),
#             'core/signin.html': reverse('signin'),
#         }
#         for template, reverse_name in templates_pages_names.items():
#             with self.subTest(reverse_name=reverse_name):
#                 response = self.client.get(reverse_name)
#                 self.assertTemplateUsed(response, template)
#
#         # Проверка словаря контекста главной страницы (в нём передаётся форма)
#
#
#     def test_home_page_show_correct_context(self):
#         """Шаблон home сформирован с правильным контекстом."""
#         response = self.authorized_client.get(reverse('index'))
#         # Словарь ожидаемых типов полей формы:
#         # указываем, объектами какого класса должны быть поля формы
#         form_fields = {
#             'title': forms.fields.CharField,
#             # При создании формы поля модели типа TextField
#             # преобразуются в CharField с виджетом forms.Textarea
#             'text': forms.fields.CharField,
#             'slug': forms.fields.SlugField,
#             'image': forms.fields.ImageField,
#         }
#
#         # Проверяем, что типы полей формы в словаре context соответствуют ожиданиям
#         for value, expected in form_fields.items():
#             with self.subTest(value=value):
#                 form_field = response.context.get('form').fields.get(value)
#                 # Проверяет, что поле формы является экземпляром
#                 # указанного класса
#                 self.assertIsInstance(form_field, expected)
#
#         # Проверяем, что словарь context страницы /task
#         # в первом элементе списка object_list содержит ожидаемые значения
#
#     def test_task_list_page_show_correct_context(self):
#         """Шаблон task_list сформирован с правильным контекстом."""
#         response = self.authorized_client.get(reverse('deals:task_list'))
#         # Взяли первый элемент из списка и проверили, что его содержание
#         # совпадает с ожидаемым
#         first_object = response.context['object_list'][0]
#         task_title_0 = first_object.title
#         task_text_0 = first_object.text
#         task_slug_0 = first_object.slug
#         self.assertEqual(task_title_0, 'Заголовок')
#         self.assertEqual(task_text_0, 'Текст')
#         self.assertEqual(task_slug_0, 'test-slug')
#
#         # Проверяем, что словарь context страницы task/test-slug
#         # содержит ожидаемые значения
#
#     def test_task_detail_pages_show_correct_context(self):
#         """Шаблон task_detail сформирован с правильным контекстом."""
#         response = (self.authorized_client.
#                     get(reverse('deals:task_detail', kwargs={'slug': 'test-slug'})))
#         self.assertEqual(response.context.get('task').title, 'Заголовок')
#         self.assertEqual(response.context.get('task').text, 'Текст')
#         self.assertEqual(response.context.get('task').slug, 'test-slug')


class IndexTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan')
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.profile = Profile.objects.create(user=self.user)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/signin?next=/')

    def test_logged_in_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse('index'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'ivan')
        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'core/index.html')

    # def test_list_of_subscriptions(self):
    #     resp = self.authorized_client.get(reverse('index'))
    #
    #     self.user2 = User.objects.create_user(username='user2')
    #     self.profile2 = Profile.objects.create(user=self.user2)
    #     self.post_by_user2 = Post.objects.create(user=self.user2, caption='123', image='blank_profile.png')
    #     # self.post_by_user = Post.objects.create(user=self.user, image='blank_profile.png')
    #     self.profile.following.add(self.profile2)
    #     print(resp.context['posts1'])
    #     print(resp.context)
    #
    #     self.assertEqual(len(resp.context['user_friends_posts']), 1)


class EditPostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png')

        self.url_edit_post1_url = reverse('edit-post', kwargs={'post_id': self.post_by_user1.id})
        self.url_edit_post2_url = reverse('edit-post', kwargs={'post_id': self.post_by_user2.id})

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('edit-post', kwargs={'post_id': '1'}))
        self.assertRedirects(response, '/signin?next=/edit-post/1/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_correct_template_GET(self):
        response = self.authorized_client.get(self.url_edit_post1_url)
        # # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'user1')
        # # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'core/edit_post.html')

    def test_author_is_able_edit_post_GET(self):
        response = self.authorized_client.get(self.url_edit_post1_url)
        self.assertEqual(response.status_code, 200)

    def test_not_author_is_not_able_edit_post_GET(self):
        response = self.authorized_client.get(self.url_edit_post2_url)
        self.assertEqual(response.status_code, 404)

    def test_author_is_able_edit_post_POST(self):
        response = self.authorized_client.post(self.url_edit_post1_url, {
            'caption': 'new_text'
        })
        self.assertEquals(response.status_code, 302)

    def test_not_author_is_not_able_edit_post_POST(self):
        response = self.authorized_client.post(self.url_edit_post2_url, {
            'caption': 'new_text'
        })
        self.assertEquals(response.status_code, 404)

    def test_edit_post_data_POST(self):
        new_image = get_image_file()
        response = self.authorized_client.post(self.url_edit_post1_url, {
            'caption': 'new_text',
            'image': new_image
        })

        self.assertEquals(Post.objects.get(id=self.post_by_user1.id).caption, 'new_text')
        self.assertTrue(Post.objects.get(id=self.post_by_user1.id).image.url.startswith('/media/post_images/test'))

    def test_edit_post_no_data_POST(self):
        response = self.authorized_client.post(self.url_edit_post1_url, {
            'caption': '',
            'image': ''
        })

        self.assertEquals(Post.objects.get(id=self.post_by_user1.id).caption, '')
        self.assertEquals(Post.objects.get(id=self.post_by_user1.id).image, 'blank_profile.png')

    def test_edit_only_post_caption_data_POST(self):
        response = self.authorized_client.post(self.url_edit_post1_url, {
            'caption': 'new_caption',
            'image': ''
        })
        self.assertEquals(Post.objects.get(id=self.post_by_user1.id).caption, 'new_caption')
        self.assertEquals(Post.objects.get(id=self.post_by_user1.id).image, 'blank_profile.png')

    # def test_edit_only_post_image_data_POST(self):
    #     new_image = SimpleUploadedFile(name='new_image.jpg', content=b'', content_type='image/jpeg')
    #
    #     response = self.authorized_client.post(self.url_edit_post1_url, {
    #         'image': new_image
    #     })
    #     self.assertEquals(Post.objects.get(id=self.post_by_user1.id).caption, '123')
    #     # self.assertTrue(Post.objects.get(id=self.post_by_user1.id).image.url.startswith('/media/post_images/new_image'))
    #     print(Post.objects.get(id=self.post_by_user1.id).image.url)


class AddCommentTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_2_by_user1_block_comments = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123',
                                                                  image='blank_profile.png', disable_comments=True)
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2,  caption='123', image='blank_profile.png')

    def test_user_is_not_loggin_in_POST(self):
        redirect_url = reverse('index')

        response = self.client.post(path=reverse('add-comment'), data={
            'post_id': self.post_1_by_user2.id,
            'text': 'comment text'},
                                               HTTP_REFERER=redirect_url)
        self.assertRedirects(response, '/signin?next=/add-comment'
                                       '')

    def test_user_is_able_add_comment_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('add-comment'), data={
            'post_id': self.post_1_by_user2.id,
            'text': 'comment text'},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_is_not_able_add_comment_where_it_blocked_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('add-comment'), data={
            'post_id': self.post_2_by_user1_block_comments.id,
            'text': 'comment text'},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)

    def test_comment_data_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('add-comment'), data={
            'post_id': self.post_1_by_user2.id,
            'text': 'comment text'},
                                               HTTP_REFERER=redirect_url)
        comment_obj = PostComments.objects.get(post__id=self.post_1_by_user2.id)
        self.assertEquals(comment_obj.text, 'comment text')
        self.assertEquals(comment_obj.user.id, self.user1.id)
        self.assertEquals(comment_obj.no_of_likes, 0)


    def test_comment_with_no_data_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('add-comment'), data={
            'post_id': self.post_1_by_user2.id,
            'text': ''},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(PostComments.objects.count(), 0)


    def test_comment_with_false_data_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('add-comment'), data={
            'post_id': 0,
            'text': 'text'},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)


class LikePostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_2_by_user1_block_comments = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123',
                                                                  image='blank_profile.png', disable_comments=True)
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png')

    def test_user_is_able_like_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('like-post'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(PostLikes.objects.first().post.id, self.post_1_by_user2.id)
        self.assertEquals(PostLikes.objects.first().user.id, self.user1.id)
        self.assertEquals(PostLikes.objects.first().post.no_of_likes, 1)
        self.assertRedirects(response, '/')

    def test_user_is_able_dislike_post_POST(self):
        redirect_url = reverse('index')
        self.post_1_by_user1.no_of_likes = 2
        self.post_1_by_user1.save()
        exists_like = PostLikes.objects.create(post=self.post_1_by_user1, user=self.user1)
        exists_like.save()

        response = self.authorized_client.post(path=reverse('like-post'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).no_of_likes, 1)
        self.assertRedirects(response, '/')

    def test_false_data_like_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('like-post'), data={
            'post_id': '99',},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)

    def test_like_plus_dislike_equal_zero_like_POST(self):
        redirect_url = reverse('index')

        response1 = self.authorized_client.post(path=reverse('like-post'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user2.id).no_of_likes, 1)
        self.assertEquals(PostLikes.objects.count(), 1)

        response2 = self.authorized_client.post(path=reverse('like-post'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response1.status_code, 302)
        self.assertEquals(response2.status_code, 302)
        self.assertEquals(PostLikes.objects.count(), 0)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user2.id).no_of_likes, 0)
        self.assertRedirects(response1, '/')
        self.assertRedirects(response2, '/')


class DeletePostTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_2_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png')

    def test_if_not_logged_in_POST(self):
        redirect_url = reverse('index')
        response = self.client.post(path=reverse('delete-post'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/delete-post')

    def test_owner_is_able_delete_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('delete-post'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.all().count(), 2)
        self.assertRedirects(response, '/profile/user1/')


    def test_not_owner_is_not_able_delete_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('delete-post'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.all().count(), 3)

    def test_false_data_delete_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('delete-post'), data={
            'post_id': '99'},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.all().count(), 3)


class DisablePostCommentsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png', disable_comments=False)
        self.post_2_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png', disable_comments=True)
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png', disable_comments=False)

    def test_if_not_logged_in_POST(self):
        redirect_url = reverse('index')
        response = self.client.post(path=reverse('disable-post-comments'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/disable-post-comments')
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, False)

    def test_owner_is_able_disable_post_comments_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('disable-post-comments'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, True)
        self.assertRedirects(response, '/')


    def test_not_owner_is_not_able_disable_post_comments_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('disable-post-comments'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, False)

    def test_false_data_disable_post_comments_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('disable-post-comments'), data={
            'post_id': 99},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, False)

    def test_disable_post_comments_if_already_disabled_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('disable-post-comments'), data={
            'post_id': self.post_2_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=self.post_2_by_user1.id).disable_comments, True)


class EnablePostCommentsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png', disable_comments=True)
        self.post_2_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png', disable_comments=False)
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png', disable_comments=True)

    def test_if_not_logged_in_POST(self):
        redirect_url = reverse('index')
        response = self.client.post(path=reverse('enable-post-comments'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/enable-post-comments')
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, True)

    def test_owner_is_able_enable_post_comments_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('enable-post-comments'), data={
            'post_id': self.post_1_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, False)
        self.assertRedirects(response, '/')


    def test_not_owner_is_not_able_enable_post_comments_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('enable-post-comments'), data={
            'post_id': self.post_1_by_user2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, True)

    def test_false_data_enable_post_comments_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('enable-post-comments'), data={
            'post_id': 99},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Post.objects.get(id=self.post_1_by_user1.id).disable_comments, True)

    def test_enable_post_comments_if_already_enable_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client.post(path=reverse('enable-post-comments'), data={
            'post_id': self.post_2_by_user1.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.get(id=self.post_2_by_user1.id).disable_comments, False)


class SignupTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile = Profile.objects.create(user=self.user2)

    def test_if_user_logged_in_GET(self):
        response = self.authorized_client.get(reverse('signup'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_signup_uses_correct_template_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_if_user_logged_in_POST(self):

        response = self.authorized_client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 2)
        self.assertRedirects(response, '/')

    def test_sign_up_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 3)
        self.assertRedirects(response, '/settings')

    def test_sign_up_check_data_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(User.objects.get(id=3).username, 'user3')
        self.assertEquals(User.objects.get(id=3).email, 'user3@mail.ru')
        self.assertEquals(User.objects.get(id=3).username, 'user3')

    def test_creating_user_profile_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(Profile.objects.count(), 3)
        self.assertEquals(Profile.objects.get(user__username='user3').user, User.objects.get(username='user3'))


    def test_if_passwords_are_not_equal_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user4',
        })
        self.assertEquals(Profile.objects.count(), 2)


class SigninTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.profile = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.profile = Profile.objects.create(user=self.user2)

    def test_if_user_already_logged_in_GET(self):
        response = self.authorized_client.get(reverse('signin'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('signin'))
        self.assertEquals(response.status_code, 200)

    def test_signin_uses_correct_template_GET(self):
        response = self.client.get(reverse('signin'))

        self.assertTemplateUsed(response, 'core/signin.html')

    def test_if_user_already_logged_in_POST(self):

        response = self.authorized_client.post(path=reverse('signin'), data={
            'username': 'user1',
            'password': 'password',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        def test_if_data_incorrect_password_POST(self):
            response = self.client.post(path=reverse('signin'), data={
                'username': 'username',
                'password': 'incorrect_password',
            })
            messages = [m.message for m in get_messages(response.wsgi_request)]

            self.assertIn('Login or password is not correct', messages)
            self.assertEquals(response.status_code, 302)
            self.assertRedirects(response, reverse('signin'))

        def test_if_not_data_POST(self):
            response = self.client.post(path=reverse('signin'), data={
                'username': '',
                'password': '',
            })
            messages = [m.message for m in get_messages(response.wsgi_request)]

            self.assertIn('Login or password is not correct', messages)
            self.assertEquals(response.status_code, 302)
            self.assertRedirects(response, reverse('signin'))


class LogoutTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.profile = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.profile = Profile.objects.create(user=self.user2)

    def test_logged_user_logout_POST(self):
        response = self.authorized_client.post(path=reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('signin'))
        response_after_logout = self.authorized_client.get(path=reverse('index'))
        self.assertEquals(response_after_logout.status_code, 302)
        self.assertRedirects(response_after_logout, '/signin?next=/')

    def test_not_logged_user_logout_POST(self):
        response = self.client.post(path=reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('signin'))
        response_after_logout = self.client.get(path=reverse('index'))
        self.assertEquals(response_after_logout.status_code, 302)
        self.assertRedirects(response_after_logout, '/signin?next=/')


class SettingsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.profile1 = Profile.objects.create(user=self.user1)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.profile2 = Profile.objects.create(user=self.user2)
        self.authorized_client_without_profile2 = Client()
        self.authorized_client_without_profile2.force_login(self.user2)


    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('settings'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/settings')


    def test_settings_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse('settings'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/settings.html')

    def test_settings_change_data_POST(self):
        new_image = get_image_file()
        response = self.authorized_client.post(path=reverse('settings'), data={
            'profileimg': new_image,
            'bio': 'new_bio',
            'location': 'new_location',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('settings'))
        self.assertTrue(Profile.objects.get(user=self.user1).profileimg.url.startswith('/media/profile_images/test'))
        self.assertEquals(Profile.objects.get(user=self.user1).bio, 'new_bio')
        self.assertEquals(Profile.objects.get(user=self.user1).location, 'new_location')


class AddPostTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.profile1 = Profile.objects.create(user=self.user1)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('add-post'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/add-post')


    def test_settings_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse('add-post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/add_post.html')

    def test_add_post_POST(self):

        image = get_image_file()
        response = self.authorized_client.post(path=reverse('add-post'), data={
            'image': image,
            'caption': 'new_caption',
            'disable_comments': True})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/profile/{self.user1.username}/')
        self.assertEquals(Post.objects.count(), 1)
        self.assertTrue(Post.objects.first().image.url.startswith('/media/post_images/test'))
        self.assertEquals(Post.objects.first().caption, 'new_caption')
        self.assertEquals(Post.objects.first().disable_comments, True)


    def test_upload_post_user_not_auth_POST(self):

        image = get_image_file()
        response = self.client.post(path=reverse('add-post'), data={
            'image': image,
            'caption': 'new_caption',
            'disable_comments': True})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/add-post')
        self.assertEquals(Post.objects.count(), 0)


class ProfileViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.user3 = User.objects.create_user(username='user3')
        self.profile3 = Profile.objects.create(user=self.user3)

        #creating posts
        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_2_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_1_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png')

        #creating followers
        self.profile1.followers.add(self.profile2)
        self.profile1.followers.add(self.profile3)
        self.profile2.followers.add(self.profile1)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('profile', kwargs={'username': self.user1.username}))
        self.assertRedirects(response, '/signin?next=/profile/user1/')

    def test_logged_in_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse('profile', kwargs={'username': self.user1.username}))

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'core/profile.html')

    def test_data_page_profile_GET(self):
        response = self.authorized_client.get(reverse('profile', kwargs={'username': self.user1.username}))

        self.assertEquals(response.context.get('page_user_profile'), self.profile1)
        self.assertEquals(response.context.get('page_user'), self.user1)
        # self.assertEquals(response.context.get('user_posts').count(), 2)
        self.assertEquals(response.context.get('user_post_length'), 2)
        self.assertEquals(response.context.get('user_followers'), 2)
        self.assertEquals(response.context.get('user_following'), 1)


class ProfileFollowingCreateViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.user3 = User.objects.create_user(username='user3')
        self.profile3 = Profile.objects.create(user=self.user3)

    def test_not_logged_try_follow_POST(self):
        response = self.client.post(reverse('follow', kwargs={'user_id': self.user1.id}))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/user/follow/1/')
        self.assertEquals(self.profile1.followers.count(), 0)

    def test_follow_if_user_doesnt_exist_POST(self):
        response = self.authorized_client.post(reverse('follow', kwargs={'user_id': 99}))
        self.assertEquals(response.status_code, 404)

    def test_follow_data_POST(self):
        response = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        self.assertEquals(self.profile2.followers.count(), 1)
        self.assertEquals(self.profile2.followers.first(), self.profile1)
        self.assertEquals(self.profile1.following.first(), self.profile2)

    def test_follow_unfollow_POST(self):
        response_follow = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        response_unfollow = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        self.assertEquals(self.profile2.followers.count(), 0)

    def test_follow_unfollow_follow_POST(self):
        response_follow1 = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        response_unfollow = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        response_follow2 = self.authorized_client.post(reverse('follow', kwargs={'user_id': int(self.user2.id)}))
        self.assertEquals(self.profile2.followers.count(), 1)


class SearchTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.user3 = User.objects.create_user(username='user3')
        self.profile3 = Profile.objects.create(user=self.user3)

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/search')

    def test_search_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse('search'), data={
            'search_user': 'user1',})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search.html')

    def test_search_user1_GET(self):
        response = self.authorized_client.get(reverse('search'), data={
            'search_user': 'user1',})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search.html')
        self.assertEquals(response.context.get('search_user_profile_list').count(), 1)
        self.assertEquals(response.context.get('search_user_profile_list').first().user.username, 'user1')

    def test_search_3_users_GET(self):
        response = self.authorized_client.get(reverse('search'), data={
            'search_user': 'user',})
        self.assertEquals(response.context.get('search_user_profile_list').count(), 3)

    def test_search_nothing_and_get_all_users_profiles_GET(self):
        response = self.authorized_client.get(reverse('search'), data={
            'search_user': '', })
        self.assertEquals(response.context.get('search_user_profile_list').count(), 3)

    def test_search_user_which_not_exists_GET(self):
        response = self.authorized_client.get(reverse('search'), data={
            'search_user': 'abc123', })
        self.assertEquals(response.context.get('search_user_profile_list').count(), 0)


class LikeCommentTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.profile1 = Profile.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

        self.client = Client()

        self.authorized_client1 = Client()
        self.authorized_client1.force_login(self.user1)

        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)


        self.post_1_by_user1 = Post.objects.create(user=self.user1, user_profile=self.profile1, caption='123', image='blank_profile.png')
        self.post_2_by_user2 = Post.objects.create(user=self.user2, user_profile=self.profile2, caption='123', image='blank_profile.png')

        self.comment_by_user1_for_post2 = PostComments.objects.create(user=self.user1, user_profile=self.profile1, text='great!', post=self.post_2_by_user2, no_of_likes=0)
        self.comment_by_user2_for_post1 = PostComments.objects.create(user=self.user2, user_profile=self.profile2, text='not bad!', post=self.post_1_by_user1, no_of_likes=3)


    def test_user_is_able_like_comment_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client1.post(path=reverse('like-comment'), data={
            'comment_id': self.comment_by_user1_for_post2.id,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(CommentLikes.objects.first().user, self.user1)
        self.assertEquals(CommentLikes.objects.first().comment, self.comment_by_user1_for_post2)
        self.assertEquals(CommentLikes.objects.count(), 1)
        self.assertRedirects(response, '/')

    def test_user_is_able_dislike_post_POST(self):
        redirect_url = reverse('index')
        self.like_by_user_2 = CommentLikes.objects.create(comment=self.comment_by_user2_for_post1, user=self.user2)

        response = self.authorized_client2.post(path=reverse('like-comment'), data={
            'comment_id': self.comment_by_user1_for_post2.id, },
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(CommentLikes.objects.count(), 2)


    def test_false_data_like_post_POST(self):
        redirect_url = reverse('index')

        response = self.authorized_client1.post(path=reverse('like-comment'), data={
            'comment_id': 99,},
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response.status_code, 404)

    def test_like_plus_dislike_equal_zero_like_POST(self):
        redirect_url = reverse('index')

        response1 = self.authorized_client1.post(path=reverse('like-comment'), data={
            'comment_id': self.comment_by_user1_for_post2.id, },
                                               HTTP_REFERER=redirect_url)
        response2 = self.authorized_client1.post(path=reverse('like-comment'), data={
            'comment_id': self.comment_by_user1_for_post2.id, },
                                               HTTP_REFERER=redirect_url)
        self.assertEquals(response1.status_code, 302)
        self.assertEquals(response2.status_code, 302)
        self.assertEquals(CommentLikes.objects.count(), 0)


#Write test for messages after finished VIEW