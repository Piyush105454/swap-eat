from django.db import models
from django.contrib.auth.models import User


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - OTP: {self.otp}"


class Invitation(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.email}"


class UserProfile(models.Model):
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
        return self.message_set.all()

    def create_new_room_message(self, sender, message):
        """Creates a new message in this room."""
        new_message = Message.objects.create(room=self, sender=sender, message=message)
        return new_message


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room: {self.room.room_name}, Sender: {self.sender}, Message: {self.message[:20]}"


class FoodPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the user
    photo = models.ImageField(upload_to="food_photos/")
    latitude = models.FloatField(null=True, blank=True)  # Auto-detected location
    longitude = models.FloatField(null=True, blank=True)  # Auto-detected location
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)  # Fixed missing max_length
    location = models.CharField(max_length=255)  # Fixed missing max_length
    radius = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.name} by {self.user.username} at {self.location} "
            f"({self.latitude}, {self.longitude}), "
            f"Radius: {self.radius} km, "
            f"Description: {self.description}, "
            f"Photo: {self.photo.url if self.photo else 'No photo'}"
        )
