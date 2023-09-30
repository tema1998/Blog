from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from .models import Profile, Post, PostLikes, PostComments, CommentLikes, Chat, Message
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from itertools import chain
import random
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, MessageForm

from .services import get_current_user, get_user_profile_by_username, get_user_friends_feeds_list_by_userprofile, \
    get_user_friends_suggestions, get_post_by_id, disable_comments, enable_comments, check_if_comment_disable, \
    if_user_is_post_owner
from .utils import UserProfileMixin
from django.http import JsonResponse


class Index(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        list_of_subscriptions = request.user.profiles.first().following.values_list('id', flat=True)

        list_of_posts = Post.objects.all().filter(user__id__in=list_of_subscriptions)

        user_friends_suggestions = get_user_friends_suggestions(request)

        return render(request, 'core/index.html', {'posts': list_of_posts,
                                                   'suggestions_username_profile_list': user_friends_suggestions[:5]})


class EditPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, post_id):

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except:
                raise Http404
        else:
            raise Http404

        user_friends_suggestions = get_user_friends_suggestions(request)

        return render(request, 'core/edit_post.html', {'post': post,
                                                       'suggestions_username_profile_list': user_friends_suggestions[
                                                                                            :5]})
    def post(self, request, post_id):
        post = get_post_by_id(post_id)
        new_image = request.FILES.get('image_upload')
        new_caption = request.POST['caption']
        if if_user_is_post_owner(request, post_id):
            if new_image:
                post.image = new_image
            post.caption = new_caption
            post.save()
            return redirect('profile', username=post.user.username)
        else:
            raise Http404

class AddComment(LoginRequiredMixin, View):
    def post(self, request):
        user = get_current_user(request)
        post = get_post_by_id(request.POST['post_id'])
        if check_if_comment_disable(post):
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.post = Post.objects.get(id=request.POST['post_id'])
                form.user = user
                form.no_of_likes = 0
                form.save()
            return redirect(request.META.get('HTTP_REFERER'))


class LikePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        username = request.user.username
        post_id = request.GET.get('post_id')

        post = Post.objects.get(id=post_id)
        like_filter = PostLikes.objects.filter(post_id=post_id, username=username).first()
        if like_filter == None:
            new_like = PostLikes.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes += 1
            post.save()
            return redirect('/')
        else:
            like_filter.delete()
            post.no_of_likes -= 1
            post.save()
            return redirect('/')


class DeletePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        if if_user_is_post_owner(request, post_id):
            post.delete()
        return redirect('profile', username=post.user.username)


class DisablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post_id = request.POST['post_id']
        if if_user_is_post_owner(request, post_id):
            disable_comments(post_id)
        return redirect(request.META.get('HTTP_REFERER'))


class EnablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post_id = request.POST['post_id']
        if if_user_is_post_owner(request, post_id):
            enable_comments(post_id)
        return redirect(request.META.get('HTTP_REFERER'))


class Signup(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)

                # Create profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    def get(self, request):
        return render(request, 'core/signup.html')


class Signin(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Login or password is not correct')
            return redirect('signin')

    def get(self, request):
        return render(request, 'core/signin.html')


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('signin')


class Settings(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        user = request.user
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        if request.POST['email'] != user.email:
            email = request.POST['email']
            user.email = email
            user.save()

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    def get(self, request):
        return render(request, 'core/settings.html', {})


class Upload(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save
        return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request):
        return redirect('/')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, username):
        page_user = User.objects.get(username=username)
        page_user_profile = Profile.objects.get(user=page_user)
        user_posts = Post.objects.filter(user=page_user)
        user_post_length = len(user_posts)

        user_followers = len(page_user_profile.followers.all())
        user_following = len(page_user_profile.following.all())

        context = {
            'page_user_profile': page_user_profile,
            'page_user': page_user,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        return render(request, 'core/profile.html', context)


class ProfilePostView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, pk, post_id):
        filter_post_id = [i for i in post_id if i != '-']
        # print(filter_post_id)
        # current_post = Post.objects.get(id=post_id)
        # print(current_post.caption)
        page_user = User.objects.get(username=pk)
        page_user_profile = Profile.objects.get(user=page_user)
        user_posts = Post.objects.filter(user=page_user)
        user_post_length = len(user_posts)

        user_followers = len(page_user_profile.followers.all())
        user_following = len(page_user_profile.following.all())

        context = {
            'page_user_profile': page_user_profile,
            'page_user': page_user,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        return render(request, 'core/profile.html', context)


class ProfileFollowingCreateView(View):
    """
    Создание подписки для пользователей
    """
    model = Profile

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, user_id):
        # user's Profile whom page
        user = self.model.objects.get(user_id=user_id)

        # user's Profile who want to follow
        profile = Profile.objects.get(user=request.user)
        # print(profile)

        if profile in user.followers.all():
            user.followers.remove(profile)
            message = f'Подписаться на {user}'
            status = False
        else:
            user.followers.add(profile)
            message = f'Отписаться от {user}'
            status = True
        data = {
            'username': profile.user.username,
            'user_id': profile.user_id,
            'message': message,
            'status': status,
        }
        return JsonResponse(data, status=200)


class Search(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(user_id=ids)
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
        return render(request, 'core/search.html',
                      {'user_object': user_profile, 'username_profile_list': username_profile_list})


class Likecomment(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        username = request.user.username
        comment_id = request.GET.get('comment_id')

        comment = PostComments.objects.get(id=comment_id)
        like_filter = CommentLikes.objects.filter(comment_id=comment_id, username=username).first()
        if like_filter == None:
            new_like = CommentLikes.objects.create(comment_id=comment_id, username=username)
            new_like.save()
            comment.no_of_likes += 1
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            like_filter.delete()
            comment.no_of_likes -= 1
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))


class DialogsView(UserProfileMixin, LoginRequiredMixin, ListView):
    login_url = 'signin'

    context_object_name = 'chats'
    model = Chat
    template_name = 'core/dialogs.html'

    def get_queryset(self):
        return Chat.objects.filter(members__in=[self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add = self.get_user_context()
        return dict(list(context.items()) + list(add.items()))


# class MessagesView(UserProfileMixin, LoginRequiredMixin, ListView):
#     login_url = 'signin'
#     slug_field = 'chat_id'
#     context_object_name = 'messages'
#     template_name = 'core/messages.html'
#
#     def get_queryset(self):
#         chat_id = self.kwargs.get('slug')
#         # Protect for writing myself
#         if chat_id == 0:
#             chat = None
#             messages = None
#             users_in_chat = None
#         else:
#             # Make a list with user's chat
#             chats = Chat.objects.filter(members=self.request.user)
#             users_in_chat = set()
#             id = self.request.user.id
#             for chat in chats:
#                 try:
#                     users_in_chat.add(chat.members.exclude(id=id)[0])
#                 except:
#                     pass
#
#             # Find messages for a chat
#             try:
#                 chat = Chat.objects.get(id=chat_id)
#                 len_messages = len(chat.message_set.all())
#                 if len_messages > 8:
#                     delta = len_messages - 8
#                     messages = chat.message_set.all().order_by('pub_date')[len_messages - delta:]
#                 else:
#                     messages = chat.message_set.all().order_by('pub_date')
#                 if self.request.user in chat.members.all():
#                     chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
#                 else:
#                     chat = None
#             except Chat.DoesNotExist:
#                 chat = None
#         return messages
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['users_in_chat'] =
#         context['chat'] =
#         add = self.get_user_context()
#         return dict(list(context.items()) + list(add.items()))

class MessagesView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, chat_id):

        # Protect for writing myself
        if chat_id == 0:
            chat = None
            messages = None
            users_in_chat = None
        else:
            # Make a list with user's chat
            chats = Chat.objects.filter(members=request.user)
            users_in_chat = set()
            id = request.user.id
            for chat in chats:
                try:
                    users_in_chat.add(chat.members.exclude(id=id)[0])
                except:
                    pass

            # Find messages for a chat
            try:
                chat = Chat.objects.get(id=chat_id)
                len_messages = len(chat.message_set.all())
                if len_messages > 8:
                    delta = len_messages - 8
                    messages = chat.message_set.all().order_by('pub_date')[len_messages - delta:]
                else:
                    messages = chat.message_set.all().order_by('pub_date')
                if request.user in chat.members.all():
                    chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
                else:
                    chat = None
            except Chat.DoesNotExist:
                chat = None

        return render(
            request,
            'core/messages.html',
            {
                'chat': chat,
                'messages': messages,
                'form': MessageForm(),
                'users_in_chat': users_in_chat,
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):  # Добавить защиту от создания диалогов с самим собой!
    def get(self, request, user_id):
        if request.user.id == user_id:
            return redirect(reverse('messages', kwargs={'chat_id': 0}))
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))
