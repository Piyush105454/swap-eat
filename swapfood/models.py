from django.db import models

# Create your models here.
class user(models.Model):
    pic = models.ImageField(upload_to="profiles")
class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    
    def return_room_messages(self):

        return Message.objects.filter(room=self)
    
    def create_new_room_message(self, sender, message):

        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)
