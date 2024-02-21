import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import User

from core.models import Profile
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer for creating connection.
    """
    async def connect(self):
        """
        Creating connection.
        """
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        """
        Break connection.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from JS,
        send message to channel group
        and call saving message to DB.
        """
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chat = data['chat']

        (message_id, date_added) = await self.save_message(username, chat, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat': chat,
                'message_id': message_id,
                'date_added': date_added,
            }
        )

    async def chat_message(self, event):
        """
        Listen channel, if user send message -
        send it to the group
        """
        message = event['message']
        username = event['username']
        chat = event['chat']
        message_id = event['message_id']
        user_profileimg_url = await(self.get_user_profile_img_url(username))
        date_added = event['date_added']


        await self.send(text_data=json.dumps({
            'message_id': message_id,
            'message': message,
            'username': username,
            'chat': chat,
            'user_profile_img_url': user_profileimg_url,
            'date_added': date_added,
        }))

    @sync_to_async
    def get_date_added(self):
        """
        Return date of sending message.
        """
        date_added = str(datetime.now())
        return date_added

    @sync_to_async
    def get_user_profile_img_url(self, username):
        """
        Return user's profile photo.
        """
        user = User.objects.get(username=username)
        user_profileimg_url = Profile.objects.get(id=user.id).profileimg.url
        return user_profileimg_url

    @sync_to_async
    def save_message(self, username, chat, message):
        """
        Save message to DB.
        """
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(id=user.id)
        chat = Chat.objects.get(id=chat)

        message = Message.objects.create(user=user, user_profile=user_profile, chat=chat, content=message)
        chat.last_update = datetime.now()
        chat.save()
        return message.id, str(message.date_added.strftime("%d-%m-%Y %H:%M"))

