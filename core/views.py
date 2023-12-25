from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from .models import Profile, Post, PostLikes, PostComments, CommentLikes, UserFavoritePosts
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .services import get_current_user, get_post_by_id, disable_comments, enable_comments, check_if_comment_disable, \
    if_user_is_post_owner, if_user_is_authenticated

from .forms import CommentForm, SignupForm, SigninForm, SettingsForm, AddPostForm, EditPostForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class Index(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        current_user_profile = Profile.objects.select_related('user').prefetch_related('following').get(
            user_id=request.user.id)
        list_of_subscriptions = current_user_profile.following.values_list('id', flat=True)

        list_of_posts = Post.objects.select_related('user', 'user_profile').prefetch_related('postcomments_set',
                                                                                             'postcomments_set__user',
                                                                                             'postcomments_set__user_profile',
                                                                                             ) \
            .only('user__username', 'user__id', 'user_profile__profileimg', 'id', 'image', 'caption', 'created_at',
                  'no_of_likes',
                  'disable_comments').filter(
            Q(user__id__in=list_of_subscriptions) | Q(user__id__in=[request.user.id])).order_by('-created_at')

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
            'user_friends_posts': user_friends_posts,})


# def load_comments(request):
#     if is_ajax(request):
#         comment = PostComments.objects.all().first()
#         return render(request, 'core/comments_ajax.html', {'comment': comment, })


class EditPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, post_id):
        try:
            post = get_post_by_id(post_id)
        except Exception:
            raise Http404

        if not post.user == request.user:
            raise Http404

        edit_post_form = EditPostForm(instance=post)

        return render(request, 'core/edit_post.html', {'edit_post_form': edit_post_form,
                                                       'post': post,
                                                       })

    def post(self, request, post_id):
        try:
            post = get_post_by_id(post_id)
        except Exception:
            raise Http404

        if not if_user_is_post_owner(post, request.user):
            raise Http404

        edit_post_form = EditPostForm(request.POST, request.FILES, instance=post)
        if edit_post_form.is_valid():
            edit_post_form.save()
            return redirect('edit-post', post_id=post.id)
        return render(request, 'core/edit_post.html', {'edit_post_form': edit_post_form,
                                                       'post': post,
                                                       })


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
                form.user_profile = Profile.objects.get(user_id=user.id)
                form.no_of_likes = 0
                form.save()
            else:
                return redirect(request.META.get('HTTP_REFERER'), {'form': form})
            return redirect(request.META.get('HTTP_REFERER'))


class LikePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, post_id):
        if is_ajax(request):
            try:
                user = get_current_user(request)
                post = get_post_by_id(post_id)

            except Exception:
                raise Http404

            liked_post = PostLikes.objects.filter(post=post, user=user).first()
            if liked_post is None:
                new_like = PostLikes.objects.create(post=post, user=user)
                new_like.save()
                post.no_of_likes += 1
                post.save()
                like_status = True

            else:
                liked_post.delete()
                post.no_of_likes -= 1
                post.save()
                like_status = False

            likes = post.no_of_likes
            data = {
                'likes': likes,
                'like_status': like_status,
            }
            return JsonResponse(data, status=200)

        # if is_ajax(request):
        #     try:
        #         current_user_id = int(request.user.id)
        #         current_user_profile = Profile.objects.get(user_id=current_user_id)
        #         post = Post.objects.get(id=post_id)
        #     except Exception:
        #         raise Http404
        #
        #     if UserFavoritePosts.objects.filter(user_profile=current_user_profile).first():
        #         user_favorites_obj = UserFavoritePosts.objects.get(user_profile=current_user_profile)
        #         if not post in user_favorites_obj.posts.all():
        #             user_favorites_obj.posts.add(post)
        #             message = f'Remove from favorites'
        #             post_status = True
        #         else:
        #             user_favorites_obj.posts.remove(post)
        #             message = f'Add to favorites'
        #             post_status = False
        #     else:
        #         user_favorites_obj = UserFavoritePosts.objects.create(user_profile=current_user_profile)
        #         user_favorites_obj.posts.add(post)
        #         message = f'Remove from favorites'
        #         post_status = True
        #
        #     data = {
        #         'message': message,
        #         'post_status': post_status,
        #     }
        #
        #     return JsonResponse(data, status=200)


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
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                with transaction.atomic():
                    new_user = signup_form.save(commit=False)
                    new_user.set_password(signup_form.cleaned_data['password'])
                    new_user.save()

                    auth.login(request, new_user)

                    # Create profile object
                    user_model = User.objects.get(username=new_user.username)
                    new_profile = Profile.objects.create(user=user_model)
                    new_profile.save()
                    return redirect('settings')
            return render(request, 'core/signup.html', {'signup_form': signup_form})

    def get(self, request):
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            signup_form = SignupForm()
            return render(request, 'core/signup.html', {'signup_form': signup_form})


class Signin(View):
    def post(self, request):
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            signin_form = SigninForm(request.POST)
            if signin_form.is_valid():
                cd = signin_form.cleaned_data
                user = auth.authenticate(username=cd['username'], password=cd['password'])
                if user:
                    auth.login(request, user)
                    return redirect('index')
            messages.error(request, f'Invalid username or password')
            return render(request, 'core/signin.html', {'signin_form': signin_form})

    def get(self, request):
        if if_user_is_authenticated(request):
            return redirect('index')
        else:
            signin_form = SigninForm()
            return render(request, 'core/signin.html', {'signin_form': signin_form})


class Logout(View):
    def post(self, request):
        auth.logout(request)
        return redirect('signin')


class Settings(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.get(user=current_user)
        settings_form = SettingsForm(request.POST, request.FILES, instance=current_user_profile)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')
        return render(request, 'core/settings.html', {'settings_form': settings_form})

    def get(self, request):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.select_related('user').only('bio', 'profileimg', 'location'
                                                                           , 'user__username') \
            .get(user=current_user)

        settings_form = SettingsForm(instance=current_user_profile)
        return render(request, 'core/settings.html', {'settings_form': settings_form})


class AddPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        add_post_form = AddPostForm()

        return render(request, 'core/add_post.html', {'add_post_form': add_post_form,})

    def post(self, request):
        user_id = int(request.user.id)
        user = User.objects.get(id=user_id)
        user_profile = Profile.objects.get(user_id=user_id)

        add_post_form = AddPostForm(request.POST, request.FILES)
        if add_post_form.is_valid():
            image = add_post_form.cleaned_data['image']
            caption = add_post_form.cleaned_data['caption']
            disable_comments = add_post_form.cleaned_data['disable_comments']
            new_post = Post.objects.create(user=user, user_profile=user_profile, image=image, caption=caption,
                                           disable_comments=disable_comments)
            return redirect('profile', username=user.username)
        return render(request, 'core/add_post.html', {'add_post_form': add_post_form})


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
            return render(request, 'core/profile_ajax.html',
                          {'page_user': page_user, 'user_posts': user_posts_paginator, })

        context = {
            'is_owner': is_owner,
            'is_subscribed': is_subscribed,
            'page_user_profile': page_user_profile,
            'page_user': page_user,
            'user_posts': user_posts_paginator,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        return render(request, 'core/profile.html', context)


class FollowersList(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, user_id):
        page_owner_profile = Profile.objects.get(user_id=user_id)
        page_owner_followers = page_owner_profile.followers.all()
        return render(request, 'core/followers.html', {
            'user_followers': page_owner_followers,
            'page_owner_profile': page_owner_profile})


class FollowingList(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, user_id):
        page_owner_profile = Profile.objects.get(user_id=user_id)
        page_owner_followers = page_owner_profile.following.all()

        return render(request, 'core/following.html', {
            'user_following': page_owner_followers,
            'page_owner_profile': page_owner_profile,})


class ProfileFollowingCreateView(LoginRequiredMixin, View):
    login_url = 'signin'

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, user_id):
        if is_ajax(request):
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
                message = f'Follow'
                status = False
            else:
                profile_page_owner.followers.add(profile_who_want_follow)
                message = f'Unfollow'
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
        search_user = request.GET['search_user']
        if search_user:
            search_user_profile_list = Profile.objects.select_related('user') \
                .filter(user__username__contains=search_user).only('user__username', 'user__id', 'bio', 'profileimg',
                                                                   'location')
        else:
            search_user_profile_list = Profile.objects.select_related('user').all()
        return render(request, 'core/search.html',
                      {'search_user_profile_list': search_user_profile_list,
                       })


class Likecomment(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, comment_id):
        if is_ajax(request):

            user_id = int(request.user.id)
            user = User.objects.get(id=user_id)
            comment = PostComments.objects.get(id=comment_id)

            like_filter = CommentLikes.objects.filter(comment=comment, user=user).first()
            if like_filter == None:
                new_like = CommentLikes.objects.create(comment=comment, user=user)
                new_like.save()
                comment.no_of_likes += 1
                comment.save()
                comment_status = True
                likes = comment.no_of_likes
            else:
                like_filter.delete()
                comment.no_of_likes -= 1
                comment.save()
                comment_status = False
                likes = comment.no_of_likes
            data = {
                'comment_status': comment_status,
                'likes': likes,
            }
            return JsonResponse(data, status=200)


class AddRemoveFavoritePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, post_id):
        if is_ajax(request):
            current_user = get_current_user(request)
            post = Post.objects.get(id=post_id)
            try:
                user_favorites_obj = UserFavoritePosts.objects.get(user=current_user, post__id=post_id)
                user_favorites_obj.delete()
                message = f'Add to favorites'
                post_status = False
            except:
                UserFavoritePosts.objects.create(user=current_user, post=post)
                message = f'Remove from favorites'
                post_status = True

            data = {
                'message': message,
                'post_status': post_status,
            }

            return JsonResponse(data, status=200)


class FavoritesPosts(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        current_user = get_current_user(request)
        user_favorite = UserFavoritePosts.objects.filter(user=current_user)
        user_favorite_post_id = [obj.post.id for obj in list(user_favorite)]
        user_favorite_posts = Post.objects.filter(id__in=user_favorite_post_id)

        return render(request, 'core/favorites_posts.html', {'user_favorite_posts': user_favorite_posts,
                                                             })
