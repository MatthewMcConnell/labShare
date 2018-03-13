import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'labShare.settings')

from datetime import datetime
import pytz

import django
django.setup()

from django.contrib.auth.models import User

from appLabShare.models import UserProfile, Post, Course, Lab

def populate():
    students = [
        {"username": "2281654m", "password": "HelloWorld1", "first_name": "Allan" ,"last_name": "McGuire","picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science", "email": "1234567m@student.gla.ac.uk"},
        {"username": "2266511m", "password": "HelloWorld2", "first_name": "David","last_name": "Mitchell","picture": "", "bio": "2nd year, Glasgow university", "degree": "Computing Science", "email": "3624739y@student.gla.ac.uk"},
        {"username": "2253290s", "password": "HelloWorld3", "first_name": "Ted","last_name": "Smith","picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science", "email": "2253290t@student.gla.ac.uk"},
        {"username": "2234512s", "password": "HelloWorld4", "first_name": "Oscar","last_name": "Stark","picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Economics", "email": "3842353r@student.gla.ac.uk"},
        {"username": "2263546t", "password": "HelloWorld5", "first_name": "Daniel","last_name": "Tarry","picture": "", "bio": "2nd year, Uni of Glasgow", "degree": "Economics", "email": "2356847a@student.gla.ac.uk"}
    ]

    tutors = [
        {"username": "11223344", "password": "HelloWorld6", "first_name": "Patricia", "last_name": "Wallace", "email" : "patriciawallace@gmail.com", "degree" : "computing Science", "picture": "", "bio": "i love to learn" },
        {"username": "99887766", "password": "HelloWorld7", "first_name": "Joe", "last_name": "Hart", "email" : "joehart@gmail.com", "degree" : "computing Science", "picture": "", "bio": "i adore learning" },
        {"username": "12345678", "password": "HelloWorld8", "first_name": "Van", "last_name": "der Sar", "email" : "vantheman@gmail.com", "degree" : "computing Science", "picture": "", "bio": "leaning is cool" }
    ]

    courses = [
        {"name": "CS1P", "level": 1},
        {"name": "EE1X", "level" : 1},

    ]

    posts = [
        {"content" : "hello world", "timePosted" : datetime.now().replace(tzinfo=pytz.UTC)},
        {"content" : "its ya boy dave the rave", "timePosted" : datetime.now().replace(tzinfo=pytz.UTC)}
    ]

    labs = [
        {"number" : 8},
        {"number" : 7},
        {"number" : 6}
    ]



    for course in courses:
        c = addCourse (course)
        print (c)


    for tutor in tutors:
        t = addTutor (tutor)
        print (t)


    for lab in labs:
        l = addLab (lab)
        print (l)


    for student in students:
        s = addStudent (student)
        print (s)


    for post in posts:
        p = addPost (post)
        print (p)





def addCourse (infoDict):
    c = Course.objects.get_or_create (name = infoDict["name"], level = infoDict["level"])[0]
    c.save()
    return c


def addTutor (infoDict):
    t = UserProfile.objects.get_or_create (user = addUser(infoDict),
                                           picture = infoDict["picture"],
                                           bio = infoDict["bio"],
                                           degree = infoDict["degree"],
                                           name = infoDict["name"],
                                           status = "Tutor")[0]
    t.save()
    return t


def addLab (infoDict):
    l = Lab.objects.get_or_create (labNumber = infoDict["number"],
                                   course = Course.objects.get (name = "EE1X"))[0]
    l.peopleInLab.add (UserProfile.objects.get (user = User.objects.get (username = "1234567x")))
    l.peopleInLab.add (UserProfile.objects.get (user = User.objects.get (username = "1232331b")))
    l.save()
    return l



def addStudent (infoDict):
    s = UserProfile.objects.get_or_create (user = addUser(infoDict),
                                           picture = infoDict["picture"],
                                           bio = infoDict["bio"],
                                           degree = infoDict["degree"],
                                           name = infoDict["name"],
                                           status = "Student")[0]
    s.courses.add (Course.objects.get (name = "EE1X"))
    s.save()
    return s



def addPost (infoDict):
    p = Post.objects.get_or_create (content = infoDict["content"],
                                    timePosted = infoDict["timePosted"],
                                    author = UserProfile.objects.get (user = User.objects.get (username = "1234567z")),
                                    postedIn = Lab.objects.get (labNumber = 8))[0]
    p.save()
    return p


def addUser (infoDict):
    u = User.objects.get_or_create (username = infoDict["username"],
                                      password = infoDict["password"],
                                      email = infoDict["email"])[0]
    u.save()
    return u



if __name__ == "__main__":
    print ("Starting population script...")
    populate()
