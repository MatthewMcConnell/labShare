from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course (models.Model):
    name = models.CharField(max_length = 128)
    level = models.PositiveSmallIntegerField ()

    def __str__ (self):
        return self.name


class UserProfile(models.Model):
    # links UserProfile to a user model instance
    # Has a username,password,email
    user = models.OneToOneField(User)

    # Boolean flag to tell us if they are a student or tutor
    status = models.CharField(max_length = 7, default = "Student")

    # Shared Tutor and Student attributes
    name = models.CharField(max_length = 128, default = "")
    picture = models.ImageField(upload_to='profile_images', default = "profile_images/user_image.png")
    bio = models.CharField(max_length = 128, default = "")
    degree = models.CharField(max_length = 128, default = "")
    university = models.CharField(max_length = 128, default = "")


    ## Student Only attributes ## - will just end up being null for tutors

    # The symmetrical set to false as we do not want adding friends to add both ways
    friends = models.ManyToManyField ("self", symmetrical=False)
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
    timePosted = models.DateTimeField(default=timezone.now)
    content = models.TextField ()
    # Attached files will be saved to /media/lab_files/
    attachedFile = models.FileField (upload_to='lab_files', default='')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__ (self):
        return self.content.__str__()
