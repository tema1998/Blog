from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    bio = models.TextField('Information', max_length=300, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile.png')
    location = models.CharField(max_length=100, blank=True)
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False,
                                       blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    disable_comments = models.BooleanField(default=False)


    def get_comments(self):
        return self.postcomments_set.all()

    def get_author_photo(self):
        return self.user_profile.profileimg.url

class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} likes {self.post}'


class PostComments(models.Model):
    """Комменты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='PostComments')
    text = models.TextField(verbose_name="Comment", max_length=5000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    no_of_likes = models.IntegerField(verbose_name='Likes')

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def user_photo(self):
        return(self.user_profile.profileimg.url)

    def get_users_like_comment(self):
        users = User.objects.filter(comment_id=self.comment_id)
        return(users)

class CommentLikes(models.Model):
    comment = models.ForeignKey(PostComments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))

    def get_absolute_url(self):
        return reverse('messages', kwargs={'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE, related_name='acc')
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=datetime.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

    def get_avatar(self):
        return Profile.objects.get(pk=self.author.id).profileimg.url

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.author.username})
