from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    # links UserProfile to a user model instance
    user = models.OneToOneField(User)

    # Additional attributes we wish to include
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length = 128)
    degree = models.CharField(max_length = 128)

    def __str__(self):
        return self.user.username


class Tutor (models.Model):
    # Is there any other fields????????!!!!!!!!! ##########################################
    profile = models.OneToOneField (UserProfile)
    idNumber = models.IntegerField(default = 0,unique= True)
    def __str__ (self):
        return self.profile.__str__

# NOTE :: the student model is at the bottom as it includes some classes that are declarated later on




class Course (models.Model):
    name = models.CharField(max_length = 128)
    level = models.PositiveSmallIntegerField ()

    def __str__ (self):
        return self.name


class Lab (models.Model):
    course = models.ForeignKey (Course)

    tutors = models.ManyToManyField (Tutor)

    labNumber = models.PositiveSmallIntegerField ()

    def __str__ (self):
        # "course::labNum"
        return self.course.__str__ + "::" + self.labNumber



class Post (models.Model):
    # Using User Profile as it makes it easier
    # (though might need to change if we want to discern between
    #  tutors and students in posts)
    author = models.ForeignKey (UserProfile)
    postedIn = models.ForeignKey (Lab)

    content = models.TextField ()
    timePosted = models.DateTimeField ()

    def __str__ (self):
        # "author::lab::time"
        return self.author.__str__ + "::" + self.postedIn.__str__ + "::" + self.timePosted





class Student(models.Model):
    # Inherits from the userprofile
    profile = models.OneToOneField (UserProfile)

    studentId = models.IntegerField(default = 0,unique = True)

    # The symmetrical set to false as we do not want adding friends to add both ways
    friends = models.ManyToManyField ("self", symmetrical=False)

    labs = models.ManyToManyField (Lab)
    courses = models.ManyToManyField (Course)

    def __str__ (self):
        return self.profile.__str__
