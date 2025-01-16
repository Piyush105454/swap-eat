from django.db import models

# Create your models here.
class user(models.Model):
    pic = models.ImageField(upload_to="profiles")
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Mychats(models.Model):
    me = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)
# Create your models here.
