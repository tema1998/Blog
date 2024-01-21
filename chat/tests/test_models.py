from datetime import datetime

from django.test import TestCase
from users.models import User

from chat.models import *


class ChatModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='username1', email='email1@mail.ru', password='password')
        user2 = User.objects.create_user(username='username2', email='email2@mail.ru', password='password')
        chat = Chat.objects.create()
        chat.members.add(user1)
        chat.members.add(user2)
        chat.save()

    def test_members_label(self):
        chat = Chat.objects.all().first()
        field_label = chat._meta.get_field('members').verbose_name
        self.assertEquals(field_label, 'Member')

    def test_last_update_label(self):
        chat = Chat.objects.all().first()
        field_label = chat._meta.get_field('last_update').verbose_name
        self.assertEquals(field_label, 'Date of last message')

    def test_str(self):
        chat = Chat.objects.all().first()
        expected_object_name = f'{chat.pk}'
        self.assertEquals(expected_object_name, str(chat))


class MessageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='username1', email='email1@mail.ru', password='password')
        user1_profile = Profile.objects.get(user=user1)
        user2 = User.objects.create_user(username='username2', email='email2@mail.ru', password='password')
        user2_profile = Profile.objects.get(user=user2)
        chat = Chat.objects.create()
        chat.members.add(user1)
        chat.members.add(user2)
        chat.save()
        message = Message.objects.create(chat=chat, user=user1, user_profile=user1_profile, content='content')

    def test_chat_label(self):
        message = Message.objects.all().first()
        field_label = message._meta.get_field('chat').verbose_name
        self.assertEquals(field_label, 'Chat')

    def test_user_label(self):
        message = Message.objects.all().first()
        field_label = message._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_user_profile_label(self):
        message = Message.objects.all().first()
        field_label = message._meta.get_field('user_profile').verbose_name
        self.assertEquals(field_label, 'User profile')

    def test_content_label(self):
        message = Message.objects.all().first()
        field_label = message._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Message content')

    def test_date_added_label(self):
        message = Message.objects.all().first()
        field_label = message._meta.get_field('date_added').verbose_name
        self.assertEquals(field_label, 'Date added')

    def test_str(self):
        message = Message.objects.all().first()
        expected_object_name = f'{message.pk}'
        self.assertEquals(expected_object_name, str(message))