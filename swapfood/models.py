from django.db import models
from django.contrib.auth.models import User


class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, related_name="chat_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="chat_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_chat_room_name(self):
        return f"chat_{min(self.user1.username, self.user2.username)}_{max(self.user1.username, self.user2.username)}"


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - OTP: {self.otp}"


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    radius = models.FloatField()
    image = models.ImageField(upload_to="meal_images/", blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)  # Auto-detected location
    longitude = models.FloatField(null=True, blank=True) # Auto-detected location
  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at ({self.latitude}, {self.longitude})"
        

class Invitation(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.email}"
class UserProfile(models.Model):  # Renamed from 'user' to avoid conflict with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="profiles", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name

    def return_room_messages(self):
        """Returns all messages associated with this room."""
        return Message.objects.filter(room=self)

    def create_new_room_message(self, sender, message):
        """Creates a new message in this room."""
        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"Room: {self.room.room_name}, Sender: {self.sender}, Message: {self.message[:20]}"
class FoodPost(models.Model):
    photo = models.ImageField(upload_to="food_photos/")
    latitude = models.FloatField(null=True, blank=True)  # Auto-detected location
    longitude = models.FloatField(null=True, blank=True) # Auto-detected location
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    radius = models.FloatField()
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Food Post at ({self.latitude}, {self.longitude})"
