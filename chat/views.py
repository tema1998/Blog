from typing import Any

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
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
    Check if the request is an AJAX request.

    Args:
    request: The HTTP request object.

    Returns:
    True if the request is an AJAX request, False otherwise.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class BaseView(LoginRequiredMixin, View):
    """Base view for auth-required views."""

    login_url = "signin"


class Chats(BaseView):
    """View returns user's chats."""

    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        """Handle GET requests for user's chats."""
        chats = get_chats_list(user=self.request.user)
        chats_per_page = 4
        paginator = Paginator(chats, chats_per_page)
        page = request.GET.get("page")
        try:
            chats_paginator = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            chats_paginator = paginator.page(1)

        return render(request, "chat/chats.html", {"chats": chats_paginator})


class ChatView(BaseView):
    """View returns chat with messages."""

    def get(self, request: http.HttpRequest, chat_id) -> http.HttpResponse:
        """Handle GET requests for chat messages."""
        chat = get_chat(chat_id=chat_id)
        if self.request.user not in get_chat_members(chat):
            return redirect("chats")

        chat_messages = get_chat_messages(chat=chat)
        messages_per_page = 15
        paginated_messages = Paginator(chat_messages, messages_per_page)
        page = request.GET.get("page")
        try:
            messages = paginated_messages.page(page)
        except (PageNotAnInteger, EmptyPage):
            messages = paginated_messages.page(1)

        if is_ajax(request):
            return self.render_ajax(request, messages)

        return self.render_chat(request, chat, messages)

    def render_ajax(self, request, messages):
        """Render the chat messages as HTML for AJAX requests."""
        return render(request, "chat/chat_ajax.html", {"messages": messages})

    def render_chat(self, request, chat, messages):
        """Render the chat messages as HTML for regular requests."""
        return render(
            request, "chat/chat.html", {"chat": chat, "messages": messages}
        )


class StartDialog(BaseView):
    """View starts a dialog between two users."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        """Handle POST requests for starting a dialog."""
        page_owner = get_user(user_id=request.POST.get("page_owner_id"))

        # User cannot start dialog with himself.
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


class DeleteMessage(BaseView):
    """View deletes the message and updates the last message date of chat."""

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        """Handle POST requests for deleting messages."""
        message = get_message(message_id=request.POST.get("message_id"))
        chat = message.chat

        # Delete message with ID = message_id.
        delete_message(message=message)

        # Update the date of last message.
        last_message_date = chat.messages.all().order_by("date_added")
        if last_message_date:
            date_of_last_message_update = last_message_date.last().date_added
            chat.last_update = date_of_last_message_update
            chat.save()

        return redirect(request.META.get("HTTP_REFERER"))


class DeleteChat(BaseView):
    """View deletes the chat."""

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        """Handle POST requests for deleting chats."""
        chat = get_chat(chat_id=request.POST.get("chat_id"))
        delete_chat(chat=chat)
        return redirect("chats")


class ClearChat(BaseView):
    """View clears the chat."""

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        """Handle POST requests for clearing chats."""
        chat = get_chat(chat_id=request.POST.get("chat_id"))
        clear_chat(chat=chat)
        return redirect("chats")
