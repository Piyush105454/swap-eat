from django.db import models

# Create your models here.
class user(models.Model):
    pic = models.ImageField(upload_to="profiles")

# Create your models here.
