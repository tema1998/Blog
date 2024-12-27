from chat.models import Chat, Message
from django.contrib import admin


class ChatAdmin(admin.ModelAdmin):
    """
    Admin for Chat model.
    """

    list_display = ("id", "last_update")
    list_display_links = ("id", "last_update")
    search_fields = ("id", "members")
    list_filter = ("last_update",)


class MessageAdmin(admin.ModelAdmin):
    """
    Admin for message model.
    """

    list_display = ("id", "chat", "user_profile", "date_added")
    list_display_links = ("id", "chat", "user_profile")
    search_fields = ("id", "chat", "user_profile")
    list_filter = ("date_added",)


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
