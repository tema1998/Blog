from django.contrib import admin

from chat.models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_update')
    list_display_links = ('id', 'last_update')
    search_fields = ('id', 'members')
    list_filter = ('last_update',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user_profile', 'date_added')
    list_display_links = ('id', 'chat', 'user_profile')
    search_fields = ('id', 'chat', 'user_profile')
    list_filter = ('date_added',)


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
