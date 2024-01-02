from core.models import User
from .models import Chat, Message


def get_chats_list(user):
    return Chat.objects.filter(members=user).order_by('-last_update')


def get_chat(chat_id):
    return Chat.objects.get(id=chat_id)


def get_chat_members(chat):
    return chat.members.all()


def get_chat_messages(chat):
    return Message.objects.filter(chat=chat).order_by('-date_added')


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_chat_with_two_users(first_user_id, second_user_id):
    return Chat.objects.filter(members__id=first_user_id).filter(members__id=second_user_id)


def create_chat_with_two_users(first_user, second_user):
    chat = Chat.objects.create()
    chat.members.add(first_user, second_user)
    chat.save()
    return chat


def get_message(message_id):
    return Message.objects.get(id=message_id)


def delete_message(message):
    message.delete()


def delete_chat(chat):
    chat.delete()


def clear_chat(chat):
    chat.messages.all().delete()