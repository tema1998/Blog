from typing import Any

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .services import (
    clear_chat,
    create_chat_with_two_users,
    delete_chat,
    delete_message,
    get_chat,
    get_chat_members,
    get_chat_messages,
    get_chat_with_two_users,
    get_chats_list,
    get_message,
    get_user,
)


def is_ajax(request: http.HttpRequest) -> Any:
    """
    Check if request is ajax.
    Return Any.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class Chats(LoginRequiredMixin, View):
    """
    View returns user's chats.
    """

    login_url = "signin"

    def get(
        self, request: http.HttpRequest
    ) -> http.HttpResponseRedirect | http.HttpResponse:
        chats = get_chats_list(user=self.request.user)

        chats_per_page = 4
        paginator = Paginator(chats, chats_per_page)
        page = request.GET.get("page")
        try:
            chats_paginator = paginator.page(page)
        except PageNotAnInteger:
            chats_paginator = paginator.page(1)
        except EmptyPage:
            chats_paginator = paginator.page(paginator.num_pages)

        return render(request, "chat/chats.html", {"chats": chats_paginator})


class ChatView(LoginRequiredMixin, View):
    """
    View returns chat with messages.
    """

    login_url = "signin"

    def get(self, request: http.HttpRequest, chat_id) -> http.HttpResponse:
        chat = get_chat(chat_id=chat_id)
        if self.request.user not in get_chat_members(chat):
            return redirect("chats")

        chat_messages = get_chat_messages(chat=chat)

        messages_per_page = 15
        paginated_messages = Paginator(chat_messages, messages_per_page)
        page = request.GET.get("page")
        try:
            messages = paginated_messages.page(page)
        except PageNotAnInteger:
            messages = paginated_messages.page(1)
        except EmptyPage:
            if is_ajax(request):
                return HttpResponse("")
            messages = paginated_messages.page(paginated_messages.num_pages)
        if is_ajax(request):
            return render(
                request,
                "chat/chat_ajax.html",
                {
                    "messages": messages,
                },
            )

        return render(
            request,
            "chat/chat.html",
            {
                "chat": chat,
                "messages": messages,
            },
        )


class StartDialog(LoginRequiredMixin, View):
    """
    View starts a dialog between two users.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        page_owner = get_user(user_id=request.POST.get("page_owner_id"))
        if request.user == page_owner:
            raise Http404

        chat = get_chat_with_two_users(
            first_user_id=self.request.user.id, second_user_id=page_owner.id
        )
        if chat:
            chat_id = chat.first().id
        else:
            chat_id = create_chat_with_two_users(
                first_user=self.request.user, second_user=page_owner
            ).id
        return redirect("chat", chat_id=chat_id)


class DeleteMessage(LoginRequiredMixin, View):
    """
    View deletes the message and
    update date of last message
    of chat.
    """

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        message = get_message(message_id=request.POST.get("message_id"))
        chat = message.chat
        delete_message(message=message)
        last_message_date = chat.messages.all().order_by("date_added")
        if last_message_date:
            date_of_last_message_update = last_message_date.last().date_added
            chat.last_update = date_of_last_message_update
            chat.save()
        return redirect(request.META.get("HTTP_REFERER"))


class DeleteChat(LoginRequiredMixin, View):
    """
    View deletes the chat.
    """

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        chat = get_chat(chat_id=request.POST.get("chat_id"))
        delete_chat(chat=chat)
        return redirect("chats")


class ClearChat(LoginRequiredMixin, View):
    """
    View clears the chat.
    """

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        chat = get_chat(chat_id=request.POST.get("chat_id"))
        clear_chat(chat=chat)
        return redirect("chats")
