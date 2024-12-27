from users.models import User

from .models import Chat, Message


def get_chats_list(user):
    """
    Return queryset user's chats sorted by last update time.
    """
    return (
        Chat.objects.prefetch_related("members")
        .filter(members=user)
        .order_by("-last_update")
    )


def get_chat(chat_id):
    """
    Return chat object.
    """
    return Chat.objects.get(id=chat_id)


def get_chat_members(chat):
    """
    Return queryset of chat members.
    """
    return chat.members.all()


def get_chat_messages(chat):
    """
    Return chat's messages.
    """
    return Message.objects.filter(chat=chat).order_by("-date_added")


def get_user(user_id):
    """
    Return user object.
    """
    return User.objects.get(id=user_id)


def get_chat_with_two_users(first_user_id, second_user_id):
    """
    Return chat with users by users ID's.
    """
    return Chat.objects.filter(members__id=first_user_id).filter(
        members__id=second_user_id
    )


def create_chat_with_two_users(first_user, second_user):
    """
    Create chat with two users and return chat object.
    """
    chat = Chat.objects.create()
    chat.members.add(first_user, second_user)
    chat.save()
    return chat


def get_message(message_id):
    """
    Return message object by ID.
    """
    return Message.objects.get(id=message_id)


def delete_message(message):
    """
    Delete message object.
    """
    message.delete()


def delete_chat(chat):
    """
    Delete chat object.
    """
    chat.delete()


def clear_chat(chat):
    """
    Clear chat history.
    """
    chat.messages.all().delete()
