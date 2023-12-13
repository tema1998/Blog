from django.urls import path

from . import views

urlpatterns = [
    path('', views.Chats.as_view(), name='chats'),
    path('<int:chat_id>/', views.ChatView.as_view(), name='chat'),
    path('start-dialog', views.StartDialog.as_view(), name='start-dialog'),
    path('delete-message', views.DeleteMessage.as_view(), name='delete-message'),
    path('delete-chat', views.DeleteChat.as_view(), name='delete-chat'),
    path('clear-chat', views.ClearChat.as_view(), name='clear-chat'),
]