from django.db import models
from django.contrib.auth.models import User


class Course (models.Model):
    name = models.CharField(max_length = 128)
    level = models.PositiveSmallIntegerField ()

    def __str__ (self):
        return self.name


class UserProfile(models.Model):
    # links UserProfile to a user model instance
    # Has a username,password,email,first_name,last_name
    user = models.OneToOneField(User)

    # Boolean flag to tell us if they are a student or tutor
    isStudent = models.BooleanField(default = True)

    # Shared Tutor and Student attributes
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length = 128)
    degree = models.CharField(max_length = 128)


    ## Student Only attributes ## - will just end up being null for tutors

    # The symmetrical set to false as we do not want adding friends to add both ways
    friends = models.ManyToManyField ("self", symmetrical=False)
    # labs = models.ManyToManyField (Lab)
    courses = models.ManyToManyField (Course)

    def __str__(self):
        return self.user.username


class Lab (models.Model):
    course = models.ForeignKey (Course)

    peopleInLab = models.ManyToManyField (UserProfile)

    labNumber = models.PositiveSmallIntegerField ()

    def __str__ (self):
        # "course :: labNum"
        return self.course.__str__() + " :: " + str(self.labNumber)


class Post (models.Model):
    author = models.ForeignKey (UserProfile)
    postedIn = models.ForeignKey (Lab)

    content = models.TextField ()
    timePosted = models.DateTimeField ()

    def __str__ (self):
        # "author :: lab :: time"
        return self.author.__str__() + " :: " + self.postedIn.__str__() + " :: " + self.timePosted.__str__()

