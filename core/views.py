from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from .models import Profile, Post, LikePost, FollowersCount, Commentss, LikeComments, Chat, Message
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from itertools import chain
import random
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, MessageForm
from core.utils import *


class Index(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request):
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get (user=user_object)
        posts = Post.objects.all()
        user_following_list = []
        feed = []

        user_following = FollowersCount.objects.filter(follower = request.user.username)

        for users in user_following:
            user_following_list.append(users.user)


        for username in user_following_list:
            feed_lists = Post.objects.filter(user=username)
            feed.append(feed_lists)
        feed.append(Post.objects.filter(user=request.user.username))
        feed_list = list(chain(*feed))

        # user suggestion
        all_users = User.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = User.objects.get(username=user.user)
            user_following_all.append(user_list)

        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = User.objects.filter(username = request.user.username)
        final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
        random.shuffle(final_suggestions_list)
        username_profile = []
        username_profile_list = []

        for users in final_suggestions_list:
            username_profile.append(users.id)

        for id in username_profile:
            profile_list = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_list)

        suggestions_username_profile_list = list(chain(*username_profile_list))

        return render(request, 'core/index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list' : suggestions_username_profile_list[:4]})
    # ADD COMMENTS
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = Post.objects.get(id=request.POST['post_id'])
            form.user = User.objects.get(id=request.POST['user_id'])
            form.no_of_likes = 0
            form.save()
        return redirect('/')

class Likepost(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request):
        username = request.user.username
        post_id = request.GET.get('post_id')

        post = Post.objects.get(id=post_id)
        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
        if like_filter == None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes +=1
            post.save()
            return redirect('/')
        else:
            like_filter.delete()
            post.no_of_likes -=1
            post.save()
            return redirect('/')

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
                user = User.objects.create_user(username = username, email = email, password = password1)
                user.save()

                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)

                #Create profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
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
            messages.info(request,'Login or password is not correct')
            return redirect('signin')
    def get(self, request):
        return render(request, 'core/signin.html')

class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('signin')

class Settings(LoginRequiredMixin, View):
    login_url = 'signin'
    def post(self,request):
        user_profile = Profile.objects.get(user=request.user)
        user=request.user
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        if request.POST['email'] != user.email:
            email = request.POST['email']
            user.email=email
            user.save()

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    def get(self,request):
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get (user=user_object)
        return render(request, 'core/settings.html', {'user_profile': user_profile})

class Upload(LoginRequiredMixin, View):
    login_url = 'signin'
    def post(self, request):
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save
        return redirect('/')
    def get(self, request):
        return redirect('/')

class ProfileView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, pk):
        user_object = User.objects.get(username=request.user.username)
        user_profile= Profile.objects.get(user=user_object)
        page_user_object = User.objects.get(username=pk)
        page_user_profile = Profile.objects.get(user=page_user_object)
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)

        follower = user_object.username
        user = page_user_object.username

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'
        user_followers = len(FollowersCount.objects.filter(user=pk))
        user_following = len(FollowersCount.objects.filter(follower=pk))

        context={
            'page_user_profile' : page_user_profile,
            'page_user_object' : page_user_object,
            'user_object' : user_object,
            'user_profile' : user_profile,
            'user_posts' : user_posts,
            'user_post_length' : user_post_length,
            'button_text' : button_text,
            'user_followers' : user_followers,
            'user_following' : user_following,
        }
        return render(request, 'core/profile.html', context)

class Follow(LoginRequiredMixin, View):
    login_url = 'signin'
    def post(self,request):
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    def get(self,request):
        return redirect('/')

class Search(LoginRequiredMixin, View):
    login_url = 'signin'
    def post(self,request):
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
        return render(request, 'core/search.html', {'user_object': user_profile, 'username_profile_list': username_profile_list})

class Likecomment(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request):
        username = request.user.username
        comment_id = request.GET.get('comment_id')

        comment = Commentss.objects.get(id=comment_id)
        like_filter = LikeComments.objects.filter(comment_id=comment_id, username=username).first()
        if like_filter == None:
            new_like = LikeComments.objects.create(comment_id=comment_id, username=username)
            new_like.save()
            comment.no_of_likes +=1
            comment.save()
            return redirect('/')
        else:
            like_filter.delete()
            comment.no_of_likes -=1
            comment.save()
            return redirect('/')

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
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get (user=user_object)

        #Protect for writing myself
        if chat_id == 0 :
            chat = None
            messages = None
            users_in_chat = None
        else:
            #Make a list with user's chat
            chats=Chat.objects.filter(members = request.user)
            users_in_chat = set()
            id = request.user.id
            for chat in chats:
                try:
                    users_in_chat.add(chat.members.exclude(id=id)[0])
                except:
                    pass

            #Find messages for a chat
            try:
                chat = Chat.objects.get(id=chat_id)
                len_messages=len(chat.message_set.all())
                if len_messages>8:
                    delta = len_messages-8
                    messages = chat.message_set.all().order_by('pub_date')[len_messages-delta:]
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
                'user_object': user_object,
                'user_profile': user_profile,
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

class CreateDialogView(View): #Добавить защиту от создания диалогов с самим собой!
    def get(self, request, user_id):
        if request.user.id == user_id:
            return redirect(reverse('messages', kwargs={'chat_id': 0}))
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))
