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

# class studentUser (models.Model):
#     # Will have to inherit from models.User

#     # DummyVariable DELETE ME WHEN IMPLEMENTING

#     dummy = models.CharField()




# class tutorUser (models.Model):
#     # Will have to inherit from models.User

#     # Below is a dummyVariable DELETE ME WHEN IMPLEMENTING

#     dummy = models.CharField()





# class course (models.Model):
#     name = models.CharField()
#     level = models.IntegerField()



# class post (models.Model):
#     content = models.CharField()
#     timePosted = models.TimeField()




# class lab (models.Model):
#     labNum = models.IntegerField()
