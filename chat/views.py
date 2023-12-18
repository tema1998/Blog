from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from core.models import Profile
from core.services import get_current_user, get_user_friends_suggestions
from .models import Chat, Message


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class Chats(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.select_related('user').prefetch_related('following').get(
            user=current_user)
        chats = Chat.objects.filter(members=current_user).order_by('-last_update')

        chats_per_page = 4
        paginator = Paginator(chats, chats_per_page)
        page = request.GET.get('page')
        try:
            chats_paginator = paginator.page(page)
        except PageNotAnInteger:
            chats_paginator = paginator.page(1)
        except EmptyPage:
            chats_paginator = paginator.page(paginator.num_pages)

        return render(request, 'chat/chats.html', {'chats': chats_paginator, 'current_user_profile': current_user_profile,})


class ChatView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, chat_id):
        current_user = get_current_user(request)
        current_user_profile = Profile.objects.select_related('user').prefetch_related('following').get(
            user=current_user)
        chat_obj = Chat.objects.get(id=chat_id)
        if not current_user in chat_obj.members.all():
            return redirect('chats')

        messages_set = Message.objects.filter(chat=chat_obj).order_by('-date_added')

        messages_per_page = 15
        paginator = Paginator(messages_set, messages_per_page)
        page = request.GET.get('page')
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            if is_ajax(request):
                return HttpResponse('')
            messages = paginator.page(paginator.num_pages)
        if is_ajax(request):
            return render(request, 'chat/chat_ajax.html', {'messages': messages, })

        return render(request, 'chat/chat.html', {'chat': chat_obj,'current_user': current_user,
                                                  'current_user_profile': current_user_profile,
                                                  'messages': messages,})


class StartDialog(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        current_user = get_current_user(request)
        page_owner = User.objects.get(id=request.POST.get('page_owner_id'))

        if Chat.objects.filter(members__id=current_user.id).filter(members__id=page_owner.id):
            chat_id = Chat.objects.filter(members__id=current_user.id).filter(members__id=page_owner.id).first().id
            return redirect('chat', chat_id=chat_id)

        chat = Chat.objects.create(type='D')
        chat.members.add(current_user, page_owner)
        chat.save()
        return redirect('chat', chat_id=chat.id)


class DeleteMessage(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        message = Message.objects.get(id= request.POST.get('message_id'))
        chat = message.chat
        if not user in chat.members.all():
            raise Http404
        message.delete()
        # last_message_date = chat.messages.all().order_by('date').last()
        # if last_message_date:
        #     last_message_date.last_update
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteChat(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        chat = Chat.objects.get(id=request.POST.get('chat_id'))
        if not user in chat.members.all():
            raise Http404
        chat.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class ClearChat(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        chat = Chat.objects.get(id=request.POST.get('chat_id'))
        if not user in chat.members.all():
            raise Http404
        chat.messages.all().delete()
        return redirect(request.META.get('HTTP_REFERER'))
