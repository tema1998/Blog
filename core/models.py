import uuid
from datetime import datetime

from django.db import models

from topblog import settings

from django.urls import reverse


class Profile(models.Model):
    """
    Model for storing profile's data.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE, related_name='profiles')
    bio = models.TextField('Information', max_length=300, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', verbose_name='Profile image', default='blank_profile.png')
    location = models.CharField(max_length=100, verbose_name='Location', blank=True)
    following = models.ManyToManyField('self', verbose_name='Subscriptions', related_name='followers', symmetrical=False,
                                       blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Post(models.Model):
    """
    Model for storing post's data.
    """
    id = models.UUIDField(verbose_name='Post ID', primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE, related_name='posts')
    user_profile = models.ForeignKey(Profile, verbose_name='User profile', on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(verbose_name='Post image', upload_to='post_images')
    caption = models.TextField(verbose_name='Caption', max_length=1000, blank=True)
    created_at = models.DateTimeField(verbose_name='Date of creation', default=datetime.now)
    no_of_likes = models.IntegerField(default=0, verbose_name='Number of likes')
    comments_status = models.BooleanField(default=True, verbose_name="Comments(uncheck the box to turn off the comments)")

    def __str__(self):
        return f'ID: {self.id}'

    def get_comments(self):
        return self.postcomments_set.all()

    def get_author_photo(self):
        return self.user_profile.profileimg.url

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class UserFavoritePosts(models.Model):
    """
    Model for storing favourites posts of user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User's favourite post"
        verbose_name_plural = "User's favourite posts"


class PostLikes(models.Model):
    """
    Model for likes of post.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.post}'

    class Meta:
        verbose_name = "Post like"
        verbose_name_plural = "Post likes"


class PostComments(models.Model):
    """
    Model for storing comments of post.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, verbose_name='User profile', on_delete=models.CASCADE, related_name='PostComments')
    text = models.TextField(verbose_name="Comment text", max_length=1000)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    no_of_likes = models.IntegerField(default=0, verbose_name='Comment likes')
    date = models.DateTimeField(verbose_name='Date of creation', default=datetime.now)

    def __str__(self):
        return f'Comment by {self.user} - {self.date}'

    class Meta:
        verbose_name = 'Post comment'
        verbose_name_plural = 'Post comments'

    def user_photo(self):
        return self.user_profile.profileimg.url


class CommentLikes(models.Model):
    """
    Model for storing likes of comments.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComments, verbose_name='Comment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = "Like of comment"
        verbose_name_plural = "Likes of comments"


