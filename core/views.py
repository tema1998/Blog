from typing import Any, Type

from django import http
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from users.models import User

from .forms import (
    AddPostForm,
    CommentForm,
    EditPostForm,
    SettingsForm,
    SigninForm,
    SignupForm,
)
from .services import (
    check_post_comments_status,
    count_queryset,
    create_favorite_post,
    create_like_post_obj,
    create_new_post,
    delete_favorite_post,
    disable_post_comments,
    dislike_comment,
    enable_post_comments,
    filter_user_profiles_by_username,
    get_all_user_profile_followers,
    get_all_user_profile_following,
    get_all_user_profiles,
    get_comment,
    get_comment_like,
    get_favorite_post,
    get_like_post_obj,
    get_post,
    get_posts_of_friends,
    get_user,
    get_user_favorite_posts,
    get_user_posts_select_and_prefetch,
    get_user_profile,
    like_comment,
)


def is_ajax(request: http.HttpRequest) -> Any:
    """Check whether the request is AJAX."""
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class BaseView(LoginRequiredMixin, View):
    """Base view to simplify LoginRequiredMixin."""

    login_url = "signin"


class Index(BaseView):
    """Main view, returns friend's posts."""

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return self.render_posts(
            get_posts_of_friends(user_id=self.request.user.id), request
        )

    def render_posts(self, posts, request):
        paginator = Paginator(posts, 2)
        page = request.GET.get("page")

        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)
        except EmptyPage:
            return (
                HttpResponse("")
                if is_ajax(request)
                else paginator.page(paginator.num_pages)
            )

        template = (
            "core/index_ajax.html" if is_ajax(request) else "core/index.html"
        )
        return render(
            request, template, {"user_friends_posts": paginated_posts}
        )


class EditPost(BaseView):
    """View for editing post."""

    def get(self, request: http.HttpRequest, post_id) -> http.HttpResponse:
        post = get_post(id=post_id)
        return render(
            request,
            "core/edit_post.html",
            {
                "edit_post_form": EditPostForm(instance=post),
                "post": post,
            },
        )

    def post(self, request: http.HttpRequest, post_id) -> http.HttpResponse:
        post = get_post(id=post_id)
        edit_post_form = EditPostForm(
            request.POST, request.FILES, instance=post
        )
        if edit_post_form.is_valid():
            edit_post_form.save()
            return redirect("edit-post", post_id=post.id)
        return self.get(request, post_id)


class AddComment(BaseView):
    """View for adding comment to post."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        user = self.request.user
        post = get_post(request.POST["post_id"])

        if not check_post_comments_status(post):
            raise Http404

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.user_profile = get_user_profile(user_id=user.id)
            comment.no_of_likes = 0
            comment.save()
        else:
            return redirect(request.META.get("HTTP_REFERER"), {"form": form})
        return redirect(request.META.get("HTTP_REFERER"))


class LikePost(BaseView):
    """View for adding like to post."""

    def post(self, request: http.HttpRequest, post_id) -> JsonResponse:
        if is_ajax(request):
            user = self.request.user
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

            return JsonResponse(
                {"likes": post.no_of_likes, "like_status": like_status},
                status=200,
            )
        return Http404


class DeletePost(BaseView):
    """View for deleting post."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        post = get_post(request.POST["post_id"])
        post.delete()
        return redirect(request.META.get("HTTP_REFERER"))


class DisablePostComments(LoginRequiredMixin, View):
    """
    View for disabling comments to post.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        post = get_post(request.POST["post_id"])

        disable_post_comments(post)

        return redirect(request.META.get("HTTP_REFERER"))


class EnablePostComments(LoginRequiredMixin, View):
    """
    View for enabling comments to post.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        post = get_post(request.POST["post_id"])

        enable_post_comments(post)

        return redirect(request.META.get("HTTP_REFERER"))


class Signup(View):
    """View for signing up."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect("index")

        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=signup_form.cleaned_data["username"],
                    password=signup_form.cleaned_data["password"],
                    email=signup_form.cleaned_data["email"],
                )
                auth.login(request, user)
                return redirect("settings")

        return render(
            request, "core/signup.html", {"signup_form": signup_form}
        )

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return (
            redirect("index")
            if request.user.is_authenticated
            else render(
                request, "core/signup.html", {"signup_form": SignupForm()}
            )
        )


class Signin(View):
    """View for signing in."""

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        if request.user.is_authenticated:
            return redirect("index")

        signin_form = SigninForm(request.POST)
        if signin_form.is_valid():
            user = auth.authenticate(
                username=signin_form.cleaned_data["username"],
                password=signin_form.cleaned_data["password"],
            )
            if user:
                auth.login(request, user)
                return redirect("index")

        messages.error(request, "Invalid username or password")
        return render(
            request, "core/signin.html", {"signin_form": signin_form}
        )

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return (
            redirect("index")
            if request.user.is_authenticated
            else render(
                request, "core/signin.html", {"signin_form": SigninForm()}
            )
        )


class Logout(View):
    """View for logging out."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        auth.logout(request)
        return redirect("signin")


class Settings(BaseView):
    """View for profile settings."""

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        user_profile = get_user_profile(user_id=request.user.id)
        return render(
            request,
            "core/settings.html",
            {
                "settings_form": SettingsForm(instance=user_profile),
                "user_profile": user_profile,
            },
        )

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        user_profile = get_user_profile(user_id=request.user.id)
        settings_form = SettingsForm(
            request.POST, request.FILES, instance=user_profile
        )

        if settings_form.is_valid():
            settings_form.save()
            return redirect("settings")

        return self.get(request)


class AddPost(BaseView):
    """View for adding post."""

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return render(
            request, "core/add_post.html", {"add_post_form": AddPostForm()}
        )

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        add_post_form = AddPostForm(request.POST, request.FILES)
        if add_post_form.is_valid():
            user_profile = get_user_profile(user_id=request.user.id)
            create_new_post(
                user=request.user,
                user_profile=user_profile,
                image=add_post_form.cleaned_data["image"],
                caption=add_post_form.cleaned_data["caption"],
            )
            return redirect("profile", username=request.user.username)

        return self.get(request)


class ProfileView(BaseView):
    """View returns user's page with posts and follow data."""

    def get(self, request: http.HttpRequest, username) -> http.HttpResponse:
        user_profile = get_user_profile(user_id=request.user.id)
        page_user = (
            self.request.user
            if self.request.user.username == username
            else get_user(username=username)
        )
        page_user_profile = get_user_profile(user_id=page_user.id)

        is_owner = page_user == self.request.user
        is_subscribed = (
            user_profile in get_all_user_profile_followers(page_user_profile)
            if not is_owner
            else False
        )

        user_posts = get_user_posts_select_and_prefetch(user=page_user)
        paginated_posts = self.paginate_posts(user_posts, request)

        context = {
            "is_owner": is_owner,
            "is_subscribed": is_subscribed,
            "page_user_profile": page_user_profile,
            "page_user": page_user,
            "user_posts": paginated_posts,
            "user_post_length": count_queryset(user_posts),
            "user_followers": count_queryset(
                get_all_user_profile_followers(page_user_profile)
            ),
            "user_following": count_queryset(
                get_all_user_profile_following(page_user_profile)
            ),
        }
        return render(request, "core/profile.html", context)

    def paginate_posts(self, posts, request):
        paginator = Paginator(posts, 3)
        page = request.GET.get("page")

        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return (
                HttpResponse("")
                if is_ajax(request)
                else paginator.page(paginator.num_pages)
            )


class FollowersList(BaseView):
    """View returns the profiles who are followed to user."""

    def get(self, request: http.HttpRequest, user_id) -> http.HttpResponse:
        page_owner_profile = get_user_profile(user_id=user_id)
        page_owner_followers = get_all_user_profile_followers(
            page_owner_profile
        )
        return render(
            request,
            "core/followers.html",
            {
                "user_followers": page_owner_followers,
                "page_owner_profile": page_owner_profile,
            },
        )


class FollowingList(BaseView):
    """View returns the profiles the user is followed to."""

    def get(self, request: http.HttpRequest, user_id) -> http.HttpResponse:
        page_owner_profile = get_user_profile(user_id=user_id)
        page_owner_following = get_all_user_profile_following(
            page_owner_profile
        )

        return render(
            request,
            "core/following.html",
            {
                "user_following": page_owner_following,
                "page_owner_profile": page_owner_profile,
            },
        )


class ProfileFollowingCreateView(LoginRequiredMixin, View):
    """
    View for creating a subscription.
    """

    login_url = "signin"

    def post(
        self, request: http.HttpRequest, user_id
    ) -> JsonResponse | Type[Http404]:
        if is_ajax(request):
            user_id_who_want_follow = int(self.request.user.id)
            user_who_want_follow = User.objects.get(id=user_id_who_want_follow)
            profile_who_want_follow = get_user_profile(
                user_id=user_who_want_follow.id
            )

            user_page_owner = User.objects.get(id=int(user_id))
            profile_page_owner = get_user_profile(user_id=user_page_owner.id)

            if profile_who_want_follow in profile_page_owner.followers.all():
                profile_page_owner.followers.remove(profile_who_want_follow)
                message = "Follow"
                status = False
            else:
                profile_page_owner.followers.add(profile_who_want_follow)
                message = "Unfollow"
                status = True
            data = {
                "username": user_who_want_follow.username,
                "user_id": user_who_want_follow.id,
                "message": message,
                "status": status,
            }
            return JsonResponse(data, status=200)
        else:
            return Http404


class Search(BaseView):
    """View for search profiles."""

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        search_text = request.GET.get("search_user", "")
        profiles = (
            filter_user_profiles_by_username(username=search_text)
            if search_text
            else get_all_user_profiles()
        )
        return render(
            request, "core/search.html", {"search_user_profile_list": profiles}
        )


class LikeComment(BaseView):
    """View to create or delete like to comment."""

    def post(self, request: http.HttpRequest, comment_id) -> JsonResponse:
        if is_ajax(request):
            comment = get_comment(comment_id=comment_id)
            comment_like = get_comment_like(comment=comment, user=request.user)

            if comment_like:
                dislike_comment(comment, comment_like)
                like_status = False
            else:
                like_comment(comment=comment, user=request.user)
                like_status = True

            return JsonResponse(
                {
                    "like_status": like_status,
                    "likes": comment.no_of_likes,
                },
                status=200,
            )
        raise Http404


class AddRemoveFavoritePost(BaseView):
    """View for adding/removing post from favorites."""

    def post(self, request: http.HttpRequest, post_id) -> JsonResponse:
        if is_ajax(request):
            post = get_post(id=post_id)
            try:
                favorite_post = get_favorite_post(user=request.user, post=post)
                delete_favorite_post(favorite_post)
                message = "Add to favorites"
                post_status = False
            except Exception:
                create_favorite_post(user=request.user, post=post)
                message = "Remove from favorites"
                post_status = True

            return JsonResponse(
                {
                    "message": message,
                    "post_status": post_status,
                },
                status=200,
            )
        raise Http404


class FavoritesPosts(BaseView):
    """View return user's favourite posts."""

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return render(
            request,
            "core/favorites_posts.html",
            {
                "user_favorite_posts": get_user_favorite_posts(
                    user=request.user
                ),
            },
        )
