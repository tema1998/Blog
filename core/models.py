from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, related_name='profiles')
    bio = models.TextField('Information', max_length=300, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', verbose_name='Profile image', default='blank_profile.png')
    location = models.CharField(max_length=100, verbose_name='Location', blank=True)
    following = models.ManyToManyField('self', verbose_name='Subscriptions', related_name='followers', symmetrical=False,
                                       blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})


class Post(models.Model):
    id = models.UUIDField(verbose_name='Post ID', primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, related_name='posts')
    user_profile = models.ForeignKey(Profile, verbose_name='User profile', on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(verbose_name='Post image', upload_to='post_images')
    caption = models.TextField(verbose_name='Caption', max_length=1000, blank=True)
    created_at = models.DateTimeField(verbose_name='Date of creation', default=datetime.now)
    no_of_likes = models.IntegerField(default=0, verbose_name='Number of likes')
    disable_comments = models.BooleanField(default=False, verbose_name='Comment status')

    def __str__(self):
        return f'Post by {self.user_profile} - {self.created_at}'

    def get_comments(self):
        return self.postcomments_set.all()

    def get_author_photo(self):
        return self.user_profile.profileimg.url


class UserFavoritePosts(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)


class PostLikes(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.post}'


class PostComments(models.Model):
    """Комменты"""
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, verbose_name='User profile', on_delete=models.CASCADE, related_name='PostComments')
    text = models.TextField(verbose_name="Comment text", max_length=1000)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    no_of_likes = models.IntegerField(default=0, verbose_name='Comment likes')
    date = models.DateTimeField(verbose_name='Date of creation', default=datetime.now)

    def __str__(self):
        return f'Comment by {self.user} - {self.date}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def user_photo(self):
        return self.user_profile.profileimg.url


class CommentLikes(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComments, verbose_name='Comment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes comment {self.pk}'


