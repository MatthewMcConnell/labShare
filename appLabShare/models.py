from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    

class UserProfile(models.Model):
    # links UserProfile to a user model instance
    user = models.OneToOneField(User)

    # Additional attributes we wish to include
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
