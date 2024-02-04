from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .services import get_post, disable_post_comments, enable_post_comments, check_if_post_comment_disable, \
    get_user_profile, get_posts_of_friends, get_like_post_obj, \
    create_like_post_obj, get_user, get_all_user_profile_followers, \
    get_user_posts_select_and_prefetch, count_queryset, get_all_user_profile_following, \
    filter_user_profiles_by_username, get_all_user_profiles, get_comment, dislike_comment, like_comment, \
    get_comment_like, get_favorite_post, delete_favorite_post, create_favorite_post, \
    get_user_favorite_posts, create_new_post
from .forms import CommentForm, SignupForm, SigninForm, SettingsForm, AddPostForm, EditPostForm
from users.models import User

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class Index(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        list_of_posts = get_posts_of_friends(user_id=request.user.id)

        posts_per_page = 2
        paginator = Paginator(list_of_posts, posts_per_page)
        page = request.GET.get('page')

        try:
            list_of_posts_paginated = paginator.page(page)
        except PageNotAnInteger:
            list_of_posts_paginated = paginator.page(1)
        except EmptyPage:
            if is_ajax(request):
                return HttpResponse('')
            list_of_posts_paginated = paginator.page(paginator.num_pages)
        if is_ajax(request):
            return render(request, 'core/index_ajax.html', {'user_friends_posts': list_of_posts_paginated, })

        return render(request, 'core/index.html', {
            'user_friends_posts': list_of_posts_paginated, })


class EditPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, post_id):
        post = get_post(id=post_id)
        edit_post_form = EditPostForm(instance=post)
        return render(request, 'core/edit_post.html', {'edit_post_form': edit_post_form,
                                                       'post': post,
                                                       })

    def post(self, request, post_id):
        post = get_post(id=post_id)

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
        user = request.user
        post = get_post(request.POST['post_id'])

        if check_if_post_comment_disable(post):
            raise Http404

        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.user = user
            form.user_profile = get_user_profile(user_id=request.user.id)
            form.no_of_likes = 0
            form.save()
        else:
            return redirect(request.META.get('HTTP_REFERER'), {'form': form})
        return redirect(request.META.get('HTTP_REFERER'))


class LikePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, post_id):
        if is_ajax(request):
            user = request.user
            post = get_post(post_id)

            try:
                like_post_obj = get_like_post_obj(post=post, user=user)
                like_post_obj.delete()
                post.no_of_likes -= 1
                post.save()
                like_status = False
            except Exception:
                create_like_post_obj(post=post, user=user)
                post.no_of_likes += 1
                post.save()
                like_status = True

            likes = post.no_of_likes
            data = {
                'likes': likes,
                'like_status': like_status,
            }
            return JsonResponse(data, status=200)


class DeletePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post = get_post(request.POST['post_id'])

        post.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class DisablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post = get_post(request.POST['post_id'])

        disable_post_comments(post)

        return redirect(request.META.get('HTTP_REFERER'))


class EnablePostComments(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        post = get_post(request.POST['post_id'])

        enable_post_comments(post)

        return redirect(request.META.get('HTTP_REFERER'))


class Signup(View):

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                with transaction.atomic():
                    cd = signup_form.cleaned_data
                    username = cd['username']
                    email = cd['email']
                    password = cd['password']
                    new_user = User.objects.create_user(username=username, password=password, email=email)

                    auth.login(request, new_user)

                    return redirect('settings')
            return render(request, 'core/signup.html', {'signup_form': signup_form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            signup_form = SignupForm()
            return render(request, 'core/signup.html', {'signup_form': signup_form})


class Signin(View):
    def post(self, request):
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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

    def get(self, request):
        user_profile = get_user_profile(user_id=request.user.id)
        settings_form = SettingsForm(instance=user_profile)
        return render(request, 'core/settings.html', {'settings_form': settings_form})

    def post(self, request):
        user_profile = get_user_profile(user_id=request.user.id)
        settings_form = SettingsForm(request.POST, request.FILES, instance=user_profile)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')
        return render(request, 'core/settings.html', {'settings_form': settings_form})


class AddPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        add_post_form = AddPostForm()

        return render(request, 'core/add_post.html', {'add_post_form': add_post_form, })

    def post(self, request):
        user_profile = get_user_profile(user_id=request.user.id)

        add_post_form = AddPostForm(request.POST, request.FILES)
        if add_post_form.is_valid():
            image = add_post_form.cleaned_data['image']
            caption = add_post_form.cleaned_data['caption']
            disable_comments = add_post_form.cleaned_data['disable_comments']
            create_new_post(user=request.user, user_profile=user_profile, image=image, caption=caption,
                            disable_comments=disable_comments)
            return redirect('profile', username=request.user.username)
        return render(request, 'core/add_post.html', {'add_post_form': add_post_form})


class ProfileView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, username):
        user_profile = get_user_profile(user_id=request.user.id)

        if request.user.username == username:
            page_user = request.user
            page_user_profile = user_profile
            is_owner = True
            is_subscribed = False
        else:
            page_user = get_user(username=username)
            page_user_profile = get_user_profile(user_id=page_user.id)
            is_owner = False
            is_subscribed = user_profile in get_all_user_profile_followers(user_profile=page_user_profile)

        user_posts = get_user_posts_select_and_prefetch(user=page_user)
        user_post_length = count_queryset(user_posts)

        user_followers = count_queryset(get_all_user_profile_followers(user_profile=page_user_profile))
        user_following = count_queryset(get_all_user_profile_following(user_profile=page_user_profile))

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
        page_owner_profile = get_user_profile(user_id=user_id)
        page_owner_followers = get_all_user_profile_followers(page_owner_profile)
        return render(request, 'core/followers.html', {
            'user_followers': page_owner_followers,
            'page_owner_profile': page_owner_profile})


class FollowingList(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, user_id):
        page_owner_profile = get_user_profile(user_id=user_id)
        page_owner_following = get_all_user_profile_following(page_owner_profile)

        return render(request, 'core/following.html', {
            'user_following': page_owner_following,
            'page_owner_profile': page_owner_profile, })


class ProfileFollowingCreateView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, user_id):
        if is_ajax(request):
            user_id_who_want_follow = int(request.user.id)
            user_who_want_follow = User.objects.get(id=user_id_who_want_follow)
            profile_who_want_follow = get_user_profile(user_id=user_who_want_follow.id)

            user_page_owner = User.objects.get(id=int(user_id))
            profile_page_owner = get_user_profile(user_id=user_page_owner.id)

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
        search_user_text = request.GET['search_user']
        if search_user_text:
            search_users_profile_list = filter_user_profiles_by_username(username=search_user_text)
        else:
            search_users_profile_list = get_all_user_profiles()
        return render(request, 'core/search.html',
                      {'search_user_profile_list': search_users_profile_list,
                       })


class LikeComment(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, comment_id):
        if is_ajax(request):
            comment = get_comment(comment_id=comment_id)
            comment_like = get_comment_like(comment=comment, user=request.user)

            if comment_like:
                dislike_comment(comment, comment_like)
                like_status = False
            else:
                like_comment(comment=comment, user=request.user)
                like_status = True

            data = {
                'like_status': like_status,
                'likes': comment.no_of_likes,
            }
            return JsonResponse(data, status=200)


class AddRemoveFavoritePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, post_id):
        if is_ajax(request):
            post = get_post(id=post_id)
            try:
                favorite_post = get_favorite_post(user=request.user, post=post)
                delete_favorite_post(favorite_post)
                message = f'Add to favorites'
                post_status = False
            except:
                create_favorite_post(user=request.user, post=post)
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
        user_favorite_posts = get_user_favorite_posts(user=request.user)
        return render(request, 'core/favorites_posts.html', {'user_favorite_posts': user_favorite_posts,
                                                             })
