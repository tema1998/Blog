from django.db.models import QuerySet
from users.models import User

from .models import Chat, Message


class ChatService:
    @staticmethod
    def get_chats_list(user: User) -> QuerySet[Chat]:
        """
        Return queryset of user's chats sorted by last update time.
        """
        return (
            Chat.objects.prefetch_related("members")
            .filter(members=user)
            .order_by("-last_update")
        )

    @staticmethod
    def get_chat(chat_id: int) -> QuerySet[Chat]:
        """
        Return chat object by ID.
        """
        return Chat.objects.get(id=chat_id)

    @staticmethod
    def get_chat_members(chat: Chat) -> QuerySet[Chat]:
        """
        Return queryset of chat members.
        """
        return chat.members.all()

    @staticmethod
    def get_chat_messages(chat: Chat) -> QuerySet[Chat]:
        """
        Return chat's messages.
        """
        return Message.objects.filter(chat=chat).order_by("-date_added")

    @staticmethod
    def get_user(user_id: int) -> QuerySet[User]:
        """
        Return user object by ID.
        """
        return User.objects.get(id=user_id)

    @staticmethod
    def get_chat_with_two_users(
        first_user_id: int, second_user_id: int
    ) -> QuerySet[Chat]:
        """
        Return chat that includes the specified two users.
        """
        return Chat.objects.filter(members__id=first_user_id).filter(
            members__id=second_user_id
        )

    @staticmethod
    def create_chat_with_two_users(
        first_user: User, second_user: User
    ) -> QuerySet[Chat]:
        """
        Create chat with two users and return the chat object.
        """
        chat = Chat.objects.create()
        chat.members.add(first_user, second_user)
        chat.save()
        return chat

    @staticmethod
    def get_message(message_id: int) -> QuerySet[Message]:
        """
        Return message object by ID.
        """
        return Message.objects.get(id=message_id)

    @staticmethod
    def delete_message(message: Message):
        """
        Delete message object.
        """
        message.delete()

    @staticmethod
    def delete_chat(chat: Chat):
        """
        Delete chat object.
        """
        chat.delete()

    @staticmethod
    def clear_chat(chat: Chat):
        """
        Clear chat history.
        """
        chat.messages.all().delete()
