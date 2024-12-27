from io import BytesIO

from chat.models import *
from django.core.files.base import File
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image


def get_image_file(
    name="test.png", ext="png", size=(50, 50), color=(256, 0, 0)
):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class ChatsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ivan", password="user1", email="ivan@ma.ru"
        )
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.profile = Profile.objects.get(user=self.user)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse("chats"))
        self.assertRedirects(response, "/signin?next=/chats/")

    def test_logged_in_uses_correct_template_GET(self):
        response = self.authorized_client.get(reverse("chats"))

        self.assertEqual(str(response.context["user"]), "ivan")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "chat/chats.html")


class ChatViewTest(TestCase):

    def setUp(self):
        self.user1_in_chat = User.objects.create_user(
            username="ivan1", password="user1", email="ivan@ma.ru"
        )
        self.profile1 = Profile.objects.get(user=self.user1_in_chat)
        self.user2_in_chat = User.objects.create_user(
            username="ivan2", password="user1", email="ivan@ma.ru"
        )
        self.profile2 = Profile.objects.get(user=self.user2_in_chat)
        self.user3_not_in_chat = User.objects.create_user(
            username="ivan3", password="user1", email="ivan@ma.ru"
        )
        self.profile3 = Profile.objects.get(user=self.user3_not_in_chat)
        self.client = Client()
        self.authorized_client_in_chat = Client()
        self.authorized_client_in_chat.force_login(self.user1_in_chat)
        self.authorized_client_not_in_chat = Client()
        self.authorized_client_not_in_chat.force_login(self.user3_not_in_chat)
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1_in_chat)
        self.chat.members.add(self.user2_in_chat)
        self.chat.save()

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(
            reverse("chat", kwargs={"chat_id": self.chat.id})
        )
        self.assertRedirects(response, "/signin?next=/chats/1/")

    def test_logged_in_uses_correct_template_GET(self):
        response = self.authorized_client_in_chat.get(
            reverse("chat", kwargs={"chat_id": self.chat.id})
        )

        self.assertEqual(str(response.context["user"]), "ivan1")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "chat/chat.html")

    def test_redirect_if_user_not_in_chat_GET(self):
        response = self.authorized_client_not_in_chat.get(
            reverse("chat", kwargs={"chat_id": self.chat.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chats/")

    def test_is_ajax_GET(self):
        response = self.authorized_client_in_chat.get(
            reverse("chat", kwargs={"chat_id": self.chat.id}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTemplateUsed(response, "chat/chat_ajax.html")


class StartDialogTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="ivan1", password="user1", email="ivan@ma.ru"
        )
        self.profile1 = Profile.objects.get(user=self.user1)
        self.user2 = User.objects.create_user(
            username="ivan2", password="user1", email="ivan@ma.ru"
        )
        self.profile2 = Profile.objects.get(user=self.user2)
        self.client = Client()
        self.authorized_user1 = Client()
        self.authorized_user1.force_login(self.user1)

    def test_start_dialog_POST(self):
        response = self.authorized_user1.post(
            reverse("start-dialog"),
            data={
                "page_owner_id": self.user2.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chats/1/")
        self.assertEqual(Chat.objects.all().count(), 1)

    def test_message_myself_POST(self):
        response = self.authorized_user1.post(
            reverse("start-dialog"),
            data={
                "page_owner_id": self.user1.id,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Chat.objects.all().count(), 0)


class DeleteMessageTest(TestCase):

    def setUp(self):
        self.user1_in_chat = User.objects.create_user(
            username="ivan1", password="user1", email="ivan@ma.ru"
        )
        self.profile1 = Profile.objects.get(user=self.user1_in_chat)
        self.user2_in_chat = User.objects.create_user(
            username="ivan2", password="user1", email="ivan@ma.ru"
        )
        self.profile2 = Profile.objects.get(user=self.user2_in_chat)
        self.user3_not_in_chat = User.objects.create_user(
            username="ivan3", password="user1", email="ivan@ma.ru"
        )
        self.profile3 = Profile.objects.get(user=self.user3_not_in_chat)
        self.client = Client()
        self.auth_user1_in_chat = Client()
        self.auth_user1_in_chat.force_login(self.user1_in_chat)
        self.auth_user2_in_chat = Client()
        self.auth_user2_in_chat.force_login(self.user2_in_chat)
        self.auth_user3_not_in_chat = Client()
        self.auth_user3_not_in_chat.force_login(self.user3_not_in_chat)
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1_in_chat)
        self.chat.members.add(self.user2_in_chat)
        self.chat.save()
        self.message = Message.objects.create(
            chat=self.chat,
            user=self.user1_in_chat,
            user_profile=self.profile1,
            content="content",
        )

    def test_user1_delete_his_message_POST(self):
        redirect_url = reverse("chat", kwargs={"chat_id": self.chat.id})
        response = self.auth_user1_in_chat.post(
            reverse("delete-message"),
            data={
                "message_id": self.message.id,
            },
            HTTP_REFERER=redirect_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chats/1/")
        self.assertEqual(Message.objects.all().count(), 0)


class DeleteChatTest(TestCase):

    def setUp(self):
        self.user1_in_chat = User.objects.create_user(
            username="ivan1", password="user1", email="ivan@ma.ru"
        )
        self.profile1 = Profile.objects.get(user=self.user1_in_chat)
        self.user2_in_chat = User.objects.create_user(
            username="ivan2", password="user1", email="ivan@ma.ru"
        )
        self.profile2 = Profile.objects.get(user=self.user2_in_chat)
        self.client = Client()
        self.auth_user1_in_chat = Client()
        self.auth_user1_in_chat.force_login(self.user1_in_chat)
        self.auth_user2_in_chat = Client()
        self.auth_user2_in_chat.force_login(self.user2_in_chat)
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1_in_chat)
        self.chat.members.add(self.user2_in_chat)
        self.chat.save()

    def test_user1_delete_his_chat_with_user2_POST(self):
        response = self.auth_user1_in_chat.post(
            reverse("delete-chat"),
            data={
                "chat_id": self.chat.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chats/")
        self.assertEqual(Chat.objects.all().count(), 0)


class ClearChatTest(TestCase):

    def setUp(self):
        self.user1_in_chat = User.objects.create_user(
            username="ivan1", password="user1", email="ivan@ma.ru"
        )
        self.profile1 = Profile.objects.get(user=self.user1_in_chat)
        self.user2_in_chat = User.objects.create_user(
            username="ivan2", password="user1", email="ivan@ma.ru"
        )
        self.profile2 = Profile.objects.get(user=self.user2_in_chat)
        self.client = Client()
        self.auth_user1_in_chat = Client()
        self.auth_user1_in_chat.force_login(self.user1_in_chat)
        self.auth_user2_in_chat = Client()
        self.auth_user2_in_chat.force_login(self.user2_in_chat)
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1_in_chat)
        self.chat.members.add(self.user2_in_chat)
        self.chat.save()
        self.message1 = Message.objects.create(
            chat=self.chat,
            user=self.user1_in_chat,
            user_profile=self.profile1,
            content="content",
        )
        self.message2 = Message.objects.create(
            chat=self.chat,
            user=self.user2_in_chat,
            user_profile=self.profile2,
            content="content123",
        )

    def test_user1_clear_chat_with_user2_POST(self):
        response = self.auth_user1_in_chat.post(
            reverse("clear-chat"),
            data={
                "chat_id": self.chat.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chats/")
        self.assertEqual(Message.objects.all().count(), 0)
