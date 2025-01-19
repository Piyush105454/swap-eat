import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from swapfood.models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"room_{self.room_name}"

        # Add the user to the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        try:
            data = json.loads(text_data)
            message = data['message']
            sender = data['sender']
            room_name = data['room_name']

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'message': {
                        'room_name': room_name,
                        'sender': sender,
                        'message': message
                    },
                }
            )
        except KeyError as e:
            await self.send(text_data=json.dumps({'error': f'Missing key: {str(e)}'}))

    async def send_message(self, event):
        # Extract message data from the event
        data = event['message']

        # Save the message to the database
        await self.create_message(data)

        # Send the message back to WebSocket clients
        await self.send(text_data=json.dumps({
            'message': {
                'sender': data['sender'],
                'message': data['message']
            }
        }))

    @database_sync_to_async
    def create_message(self, data):
        # Get the room object
        try:
            room = Room.objects.get(room_name=data['room_name'])
        except Room.DoesNotExist:
            return None  # Handle this case in the front end if needed

        # Save the message if it doesn't already exist
        if not Message.objects.filter(message=data['message'], room=room).exists():
            return Message.objects.create(
                room=room,
                sender=data['sender'],
                message=data['message']
            )
