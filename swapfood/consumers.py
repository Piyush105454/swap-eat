import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['user'].username
        self.other_user = self.scope['url_route']['kwargs']['username']
        
        # Create a unique room name
        sorted_users = sorted([self.username, self.other_user])
        self.room_name = f"chat_{sorted_users[0]}_{sorted_users[1]}"
        self.room_group_name = f"chat_{self.room_name}"

        # Add the user to the chat room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from chat room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ Handles incoming messages """
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user'].username

        # Save message to database
        await self.save_message(sender, message)

        # Send message to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        """ Sends message to WebSocket clients """
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def save_message(self, sender, message):
        """ Saves chat messages in the database """
        user = User.objects.get(username=sender)
        room, created = Room.objects.get_or_create(room_name=self.room_name)
        Message.objects.create(room=room, sender=user, message=message)
