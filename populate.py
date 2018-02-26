import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'labShare.settings')


import django
django.setup()
from appLabShare.models import UserProfile, Tutor, Student, Post, Course

def populate():
    students = [
        {"id": "2253468", "name": "Allan McGuire" ,"picture": "jpeg1", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science"},
        {"id": "3624739", "name": "David Mitchell" ,"picture": "jpeg2", "bio": "2nd year, Glasgow university", "degree": "Computing Science"},
        {"id": "2253290", "name": "Ted Smith" ,"picture": "jpeg3", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science"},
        {"id": "3842353", "name": "Oscar Stark" ,"picture": "jpeg4", "bio": "2nd year, Uni of Glasgow", "degree": "Economics"},
        {"id": "2356847", "name": "Daniel Tarry" ,"picture": "jpeg5", "bio": "2nd year, Uni of Glasgow", "degree": "Economics"}
    ]

    tutors = [
        {"id": "1232333", "name": "Patricia Wallace", "email" : "patriciawallace@gmail.com", "degree" : "computing Science", "picture": "jpeg6", "bio": "i love to learn" },
        {"id": "5364377", "name": "Joe Hart", "email" : "joehart@gmail.com", "degree" : "computing Science", "picture": "jpeg7", "bio": "i adore learning" },
        {"id": "1232333", "name": "Van der sar", "email" : "vantheman@gmail.com", "degree" : "computing Science", "picture": "jpeg8", "bio": "leaning is cool" }
    ]

    course = [
        {"name": "Computing Science", "level": "2"},
        {"name": "Economics", "level" : "2"},

    ]

    post = [
        {"author" : "David Mitchell", "labGroup": "8", "text" : "hello world", "date posted" : "" }
        {"author" : "David Mitchell", "labGroup": "8", "text" : "its ya boy dave the rave", "date posted" : "" }
    ]

    lab = [
        {"number" : "8"},
        {"number" : "7"},
        {"number" : "6"}
    ]
