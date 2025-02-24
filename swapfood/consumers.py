import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer

User = get_user_model()

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["username"]
        self.other_user = await self.get_user(self.other_username)

        if self.user.is_authenticated and self.other_user:
            self.room_name = f"chat_{min(self.user.username, self.other_user.username)}_{max(self.user.username, self.other_user.username)}"
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.user.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def get_user(self, username):
        try:
            return await User.objects.get(username=username)
        except User.DoesNotExist:
            return None
