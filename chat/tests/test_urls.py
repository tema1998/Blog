from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chat.views import *


class TestUrls(SimpleTestCase):

    def test_chats_url_resolves(self):
        url = reverse('chats')
        self.assertEquals(resolve(url).func.view_class, Chats)

    def test_chat_url_resolves(self):
        url = reverse('chat', args=[2213])
        self.assertEquals(resolve(url).func.view_class, ChatView)

    def test_start_dialog_url_resolves(self):
        url = reverse('start-dialog')
        self.assertEquals(resolve(url).func.view_class, StartDialog)

    def test_delete_message_url_resolves(self):
        url = reverse('delete-message')
        self.assertEquals(resolve(url).func.view_class, DeleteMessage)

    def test_delete_chat_url_resolves(self):
        url = reverse('delete-chat')
        self.assertEquals(resolve(url).func.view_class, DeleteChat)

    def test_cleat_chat_url_resolves(self):
        url = reverse('clear-chat')
        self.assertEquals(resolve(url).func.view_class, ClearChat)