from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from .models import Profile, Post, PostLikes, PostComments, CommentLikes, Chat, Message
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .services import get_current_user, get_user_profile_by_username, \
    get_user_friends_suggestions, get_post_by_id, disable_comments, enable_comments, check_if_comment_disable, \
    if_user_is_post_owner, if_user_is_authenticated, get_user_profile_by_user_object
from .utils import UserProfileMixin
from .forms import CommentForm, MessageForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class Index(LoginRequiredMixin, View):
    # login_url = 'signin'

    def get(self, request):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.select_related('user').prefetch_related('following').get(
            user=current_user)
        user_friends_suggestions = get_user_friends_suggestions(current_user_profile)
        list_of_subscriptions = current_user_profile.following.values_list('id', flat=True)

        list_of_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                             'postcomments_set__user',
                                                                                             'postcomments_set__user_profile',
                                                                                             ) \
            .only('user__username', 'user__id', 'user_profile__profileimg', 'id', 'image', 'caption', 'created_at',
                  'no_of_likes',
                  'disable_comments').filter(
            Q(user__id__in=list_of_subscriptions) | Q(user__id__in=[current_user.id])).order_by('-created_at')

        posts_per_page = 2
        paginator = Paginator(list_of_posts, posts_per_page)
        page = request.GET.get('page')
        try:
            user_friends_posts = paginator.page(page)
        except PageNotAnInteger:
            user_friends_posts = paginator.page(1)
        except EmptyPage:
            if is_ajax(request):
                return HttpResponse('')
            user_friends_posts = paginator.page(paginator.num_pages)
        if is_ajax(request):
            return render(request, 'core/index_ajax.html', {'user_friends_posts': user_friends_posts, })

        return render(request, 'core/index.html', {
            'current_user_profile': current_user_profile,
            'user_friends_posts': user_friends_posts,
            'suggestions_username_profile_list': user_friends_suggestions[:5]})


class EditPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, post_id):
        try:
            post = get_post_by_id(post_id)
            current_user = get_current_user(request)
            current_user_profile = Profile.objects.select_related('user').prefetch_related('following').get(
                user=current_user)
        except Exception:
            raise Http404

        if not post.user == current_user:
            raise Http404

        user_friends_suggestions = get_user_friends_suggestions(current_user_profile)

        return render(request, 'core/edit_post.html', {'current_user_profile': current_user_profile,
                                                       'post': post,
                                                       'suggestions_username_profile_list': user_friends_suggestions[
                                                                                            :5]})

    def post(self, request, post_id):
        try:
            user = get_current_user(request)
            post = get_post_by_id(post_id)
        except Exception:
            raise Http404
        new_image = request.FILES.get('image_upload')
        new_caption = request.POST['caption']
        if if_user_is_post_owner(post, user):
            if new_image:
                post.image = new_image
            if new_caption != post.caption:
                post.caption = new_caption
            post.save()
            return redirect('profile', username=post.user.username)
        else:
            raise Http404


class AddComment(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user = get_current_user(request)
            post = get_post_by_id(request.POST['post_id'])
        except Exception:
            raise Http404

        if check_if_comment_disable(post):
            raise Http404
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.post = Post.objects.get(id=request.POST['post_id'])
                form.user = user
                form.user_profile = Profile.objects.get(id=user.id)
                form.no_of_likes = 0
                form.save()
            else:
                messages.info(request, 'Please, enter text')
                return redirect(request.META.get('HTTP_REFERER'))
            return redirect(request.META.get('HTTP_REFERER'))


class LikePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user = get_current_user(request)
            print(user)
            post = get_post_by_id(request.POST['post_id'])

        except Exception:
            print('ne rabotaet')
            raise Http404

        liked_post = PostLikes.objects.filter(post=post, user=user).first()
        if liked_post is None:
            new_like = PostLikes.objects.create(post=post, user=user)
            new_like.save()
            post.no_of_likes += 1
            post.save()
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            liked_post.delete()
            post.no_of_likes -= 1
            post.save()
            return redirect(request.META.get('HTTP_REFERER'))


class DeletePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user = get_current_user(request)
            post = get_post_by_id(request.POST['post_id'])
        except Exception:
            raise Http404

        if post.user == user:
            post.delete()
        else:
            raise Http404

        return redirect('profile', username=post.user.username)


class DisablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user = get_current_user(request)
            post = get_post_by_id(request.POST['post_id'])
        except Exception:
            raise Http404
        if if_user_is_post_owner(post, user):
            disable_comments(post)
        else:
            raise Http404
        return redirect(request.META.get('HTTP_REFERER'))


class EnablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user = get_current_user(request)
            post = get_post_by_id(request.POST['post_id'])
        except Exception:
            raise Http404
        if if_user_is_post_owner(post, user):
            enable_comments(post)
        else:
            raise Http404
        return redirect(request.META.get('HTTP_REFERER'))


class Signup(View):

    def post(self, request):
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if not username or not email or not password1 or not password2:
                messages.info(request, 'Please fill in the blank fields')
                return redirect('signup')

            elif password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Em1ail taken')
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
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            return render(request, 'core/signup.html')


class Signin(View):
    def post(self, request):
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
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
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            return render(request, 'core/signin.html')


class Logout(View):
    def post(self, request):
        auth.logout(request)
        return redirect('signin')


class Settings(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            current_user = get_current_user(request)
            current_user_profile = Profile.objects.get(user=current_user)
        except Exception:
            raise Http404

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            current_user_profile.profileimg = image

        if request.POST['email'] != current_user.email:
            email = request.POST['email']
            current_user.email = email
            current_user.save()

        if request.POST['bio'] != current_user_profile.bio:
            bio = request.POST['bio']
            current_user_profile.bio = bio

        if request.POST['location'] != current_user_profile.location:
            location = request.POST['location']
            current_user_profile.location = location

        current_user_profile.save()
        return redirect('settings')

    def get(self, request):
        try:
            current_user = get_current_user(request)
            current_user_profile = Profile.objects.select_related('user').only('bio', 'profileimg', 'location',
                                                                               'user__email', 'user__username') \
                .get(user=current_user)
        except Exception:
            raise Http404
        return render(request, 'core/settings.html', {'current_user': current_user,
                                                      'current_user_profile': current_user_profile})


class Upload(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user_id = int(request.user.id)
            user = User.objects.get(id=user_id)
            user_profile = Profile.objects.get(id=user_id)
        except Exception:
            raise Http404

        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        if image is not None:
            new_post = Post.objects.create(user=user, user_profile=user_profile, image=image, caption=caption)
            new_post.save
        else:
            messages.info(request, 'Please, choose image!')

        return redirect(request.META.get('HTTP_REFERER'))


class ProfileView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, username):
        try:
            current_user = get_current_user(request)
            current_user_profile = Profile.objects.select_related('user').get(user=current_user)
            if current_user.username == username:
                page_user = current_user
                page_user_profile = current_user_profile
            else:
                page_user = User.objects.get(username=username)
                page_user_profile = Profile.objects.get(user=page_user)

        except Exception:
            raise Http404

        is_owner = current_user == page_user
        if not is_owner:
            is_subscribed = current_user_profile in page_user_profile.followers.all()
        else:
            is_subscribed = False
        user_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                          'postcomments_set__user',
                                                                                          'postcomments_set__user_profile', ) \
            .only('user__username', 'user__id', 'user_profile__profileimg', 'id', 'image', 'caption', 'created_at',
                  'no_of_likes',
                  'disable_comments').filter(user=page_user).order_by('-created_at')
        user_post_length = user_posts.count()

        user_followers = page_user_profile.followers.all().count()
        user_following = page_user_profile.following.all().count()

        # Pagination
        posts_per_page = 3
        paginator = Paginator(user_posts, posts_per_page)
        page = request.GET.get('page')
        try:
            user_posts_paginator = paginator.page(page)
        except PageNotAnInteger:
            user_posts_paginator = paginator.page(1)
        except EmptyPage:
            if is_ajax(request):
                return HttpResponse('')
            user_posts_paginator = paginator.page(paginator.num_pages)
        if is_ajax(request):
            return render(request, 'core/profile_ajax.html', {'user_posts': user_posts_paginator, })

        context = {
            'is_owner': is_owner,
            'is_subscribed': is_subscribed,
            'current_user_profile': current_user_profile,
            'page_user_profile': page_user_profile,
            'page_user': page_user,
            'user_posts': user_posts_paginator,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        return render(request, 'core/profile.html', context)


class ProfileFollowingCreateView(LoginRequiredMixin, View):
    login_url = 'signin'

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, user_id):
        try:
            user_id_who_want_follow = int(request.user.id)
            user_who_want_follow = User.objects.get(id=user_id_who_want_follow)
            profile_who_want_follow = Profile.objects.get(user=user_who_want_follow)

            user_page_owner = User.objects.get(id=int(user_id))
            profile_page_owner = Profile.objects.get(user=user_page_owner)

        except Exception:
            raise Http404

        if profile_who_want_follow in profile_page_owner.followers.all():
            profile_page_owner.followers.remove(profile_who_want_follow)
            message = f'Подписаться на {profile_page_owner}'
            status = False
        else:
            profile_page_owner.followers.add(profile_who_want_follow)
            message = f'Отписаться от {profile_page_owner}'
            status = True
        data = {
            'username': user_who_want_follow.username,
            'user_id': user_who_want_follow.id,
            'message': message,
            'status': status,
        }
        return JsonResponse(data, status=200)


class Search(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.select_related('user').get(user=current_user)
        try:
            search_user = request.GET['search_user']
        except:
            search_user = ''
        if search_user:
            search_user_profile_list = Profile.objects.select_related('user') \
                .filter(user__username__contains=search_user).only('user__username', 'user__id', 'bio', 'profileimg',
                                                                   'location')
        else:
            search_user_profile_list = Profile.objects.select_related('user').all()
        return render(request, 'core/search.html',
                      {'search_user_profile_list': search_user_profile_list,
                       'current_user': current_user,
                       'current_user_profile': current_user_profile})


class Likecomment(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        try:
            user_id = int(request.user.id)
            user = User.objects.get(id=user_id)
            comment_id = request.POST.get('comment_id')
            comment = PostComments.objects.get(id=comment_id)
        except Exception:
            raise Http404

        like_filter = CommentLikes.objects.filter(comment=comment, user=user).first()
        if like_filter == None:
            new_like = CommentLikes.objects.create(comment=comment, user=user)
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
