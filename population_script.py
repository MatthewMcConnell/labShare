import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'labShare.settings')

from datetime import datetime
import pytz

import django
django.setup()

from django.contrib.auth.models import User
from django.core.files import File

from registration.signals import user_registered, user_activated

from appLabShare.models import UserProfile, Post, Course, Lab

def populate():
    # Any pictures with an empty "" should automatically assign it the picture called user_image.png in the media/profile_images folder
    # for both students and tutors

    students = [
        {"username": "2281654m", "password": "HelloWorld1", "name": "Allan McGuire", "picture": "populationScriptFiles/coolAppa.jpg", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science", "email": "1234567m@student.gla.ac.uk"},
        {"username": "2266511m", "password": "HelloWorld2", "name": "David Mitchell", "picture": "populationScriptFiles/studentProfilePic.jpg", "bio": "2nd year, Glasgow university", "degree": "Computing Science", "email": "3624739y@student.gla.ac.uk"},
        {"username": "2253290s", "password": "HelloWorld3", "name": "Ted Smith", "picture": "populationScriptFiles/coolAppa.jpg", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science", "email": "2253290t@student.gla.ac.uk"},
        {"username": "2234512s", "password": "HelloWorld4", "name": "Oscar Stark", "picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Economics", "email": "3842353r@student.gla.ac.uk"},
        {"username": "2263546t", "password": "HelloWorld5", "name": "Daniel Tarry", "picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Economics", "email": "2356847a@student.gla.ac.uk"}
    ]

    tutors = [
        {"username": "11223344", "password": "HelloWorld6", "name": "Patricia Wallace", "email" : "patriciawallace@gmail.com", "degree" : "computing Science", "picture": "populationScriptFiles/tutorProfilePic.jpg", "bio": "i love to learn" },
        {"username": "99887766", "password": "HelloWorld7", "name": "Joe Hart", "email" : "joehart@gmail.com", "degree" : "computing Science", "picture": "populationScriptFiles/tutorProfilePic.jpg", "bio": "i adore learning" },
        {"username": "12345678", "password": "HelloWorld8", "name": "Van der Sar", "email" : "vantheman@gmail.com", "degree" : "computing Science", "picture": "", "bio": "leaning is cool" }
    ]

    courses = [
        {"name": "CS1P", "level": 1},
        {"name": "EE1X", "level" : 1},
        {"name": "CS2X", "level": 2},
        {"name": "CS2S", "level": 2},
        {"name": "CS2Y", "level": 2},
        {"name": "CS3004", "level": 3},
        {"name": "CS4021", "level": 4},
    ]

    posts = [
        {"content" : "hello world", "timePosted" : datetime.now().replace(tzinfo=pytz.UTC), "attachedFile" : "populationScriptFiles/lab1Tips.txt", "name" : "Patricia Wallace"},
        {"content" : "its ya boy dave the rave", "timePosted" : datetime.now().replace(tzinfo=pytz.UTC), "attachedFile" : "", "name" : "Joe Hart"},
        {"content" : "Hey guys I'm a student!", "timePosted": datetime.now().replace(tzinfo=pytz.UTC), "attachedFile": "populationScriptFiles/lab2Tips.txt", "name": "Oscar Stark"},
    ]


    print ("Courses:")
    for course in courses:
        addCourseAndLabs (course)


    print ("Tutors:")
    for tutor in tutors:
        addUserAndProfile (tutor, "Tutor")


    print ("Students:")
    for student in students:
        addUserAndProfile (student, "Student")


    print ("Enrolling tutors:")
    enrolTutors ()


    print ("Enrolling students:")
    enrolStudents ()


    print ("Posts:")
    for post in posts:
        p = addPost (post)
        print (p)


    print ("Making friends:")
    makeFriends ()


    print ()
    print ("The population script is now finished!")





def addCourseAndLabs (infoDict):
    c = Course.objects.get_or_create (name = infoDict["name"], level = infoDict["level"])[0]
    c.save()

    print (c)
    print ("Labs:")

    # Each course will get 12 labs
    addLabs (c)



def addLabs (course):
    for labNum in range(1, 13):
        l = Lab.objects.get_or_create (labNumber = labNum, course = course)[0]
        l.save()
        print (l)



def addPost (infoDict):
    p = Post.objects.get_or_create (content = infoDict["content"],
                                    timePosted = infoDict["timePosted"],
                                    author = UserProfile.objects.get (name = infoDict["name"]),
                                    postedIn = Lab.objects.get (labNumber = 4, course = Course.objects.get (name = "CS1P")))[0]
    
    if (infoDict["attachedFile"] != ""):
        p.attachedFile.save ('file.txt', File (open(infoDict["attachedFile"], 'rb')))

    p.save()
    return p



def addUserAndProfile (infoDict, status):
    user = User.objects.get_or_create (username = infoDict["username"],
                                       password = infoDict["password"],
                                       email = infoDict["email"])[0]
    user.set_password (user.password)
    user.save()

    profile = UserProfile.objects.get_or_create (user = user,
                                                 bio = infoDict["bio"],
                                                 degree = infoDict["degree"],
                                                 name = infoDict["name"],
                                                 status = status)[0]

    if (infoDict["picture"] != ""):
        profile.picture.save ('picture.jpg', File (open(infoDict["picture"], 'rb')))

    # To test on one person if the social media links work
    if (profile.name == "Allan McGuire"):
        profile.facebook = "https://www.facebook.com/musicalSpearman"

    profile.save()

    print (profile)



def enrolTutors ():
    course1 = Course.objects.get (name = "CS1P")
    course2 = Course.objects.get (name = "CS2X")

    labs1 = Lab.objects.filter (course = course1)
    labs2 = Lab.objects.filter (course = course2)

    for tutor in UserProfile.objects.filter (status = "Tutor"):
        tutor.courses.add (course1)
        tutor.courses.add (course2)

        for lab in labs1:
            lab.peopleInLab.add (tutor)
            print (tutor.__str__() + " enrolled in " + lab.__str__())

        for lab in labs2:
            lab.peopleInLab.add (tutor)
            print (tutor.__str__() + " enrolled in " + lab.__str__())



def enrolStudents ():
    course1 = Course.objects.get (name = "CS1P")
    course2 = Course.objects.get (name = "CS2X")

    labNum = 1

    for student in UserProfile.objects.filter (status = "Student"):
        student.courses.add (course1)
        student.courses.add (course2)

        # Students can only be enrolled in 1 lab per course so I am reflecting that here
        lab1 = Lab.objects.get (course = course1, labNumber = labNum)
        lab2 = Lab.objects.get (course = course2, labNumber = labNum)

        lab1.peopleInLab.add (student)
        print (student.__str__() + " enrolled in " + lab1.__str__())

        lab2.peopleInLab.add (student)
        print (student.__str__() + " enrolled in " + lab2.__str__())

        # Incrementing the lab number so that the next student is in a different lab
        labNum += 1



def makeFriends ():
    everyonesFriend = UserProfile.objects.get (name = "Allan McGuire")

    for student in UserProfile.objects.filter (status = "Student"):
        if (student != everyonesFriend):
            student.friends.add (everyonesFriend)
            print (everyonesFriend.__str__() + " has been added as " + student.__str__() + "'s friend")




if __name__ == "__main__":
    print ("Starting population script...")
    populate()
