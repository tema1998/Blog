from django.db import models
from users.models import User

from core.models import Profile


class Chat(models.Model):
    """
    Model for storing chats.
    """
    members = models.ManyToManyField(User, verbose_name='Member')
    last_update = models.DateTimeField(auto_now_add=True, verbose_name='Date of last message')

    def __str__(self):
        return f'{self.pk}'

    def get_users(self):
        """
        Return members of chat.
        """
        return self.members.all()

    def get_last_message(self):
        """
        Return last message of chat.
        """
        return self.messages.last()

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Message(models.Model):
    """
    Model for storing messages.
    """
    chat = models.ForeignKey(Chat, verbose_name='Chat', related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User,  verbose_name='User', related_name='messages', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, verbose_name='User profile', on_delete=models.CASCADE, related_name='profile')
    content = models.TextField(verbose_name='Message content')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('date_added',)

    def get_author_photo(self):
        """
        Return message's author photo.
        """
        return self.user_profile.profileimg.url

    def __str__(self):
        return f'{self.pk}'

