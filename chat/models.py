from django.db import models
from django.urls import reverse
from core.models import Profile
from django.contrib.auth.models import User


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, ('Dialog')),
        (CHAT, ('Chat'))
    )

    type = models.CharField(
        ('Type'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=("Member"))
    last_update = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('messages', kwargs={'chat_id': self.pk})

    def get_users(self):
        return self.members.all()

    def get_last_message(self):
        return self.messages.last()


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    def get_author_photo(self):
        return self.user_profile.profileimg.url