from django.test import TestCase

from populate import *

from appLabShare.models import *



class ModelTests (TestCase):
    def test_creatingCourse (self):
        c = Course(name = "CS1P", level = 2)
        c.save()

        courses = Course.objects.all()
        self.assertEqual (len(courses), 1, "Not only 1 course was made")
        course = courses[0]
        self.assertEqual (c, course, "The queried course was not equal")


    def test_creatingUserProfile (self):
        u = User (username = "1234567s",
                  password = "HelloWorld1", 
                  email = "1234567s@gmail.com")
        u.save()

        up = UserProfile (user = u,
                          status = "Student",
                          facebook = "www.facebook.com")
        up.save()


        friendUser = User (username = "1234567t", password = "HelloWorld1", email = "1234567s@gmail.com")
        friendUser.save()
        friend = UserProfile(user = friendUser)
        friend.save()

        course = Course (name = "CS1P", level = 3)
        course.save()

        up.friend = friend
        up.courses.add (course)
        
        up.save()

        userProfiles = UserProfile.objects.all()
        self.assertEqual (len(userProfiles), 2, "Not only 2 profiles were made")
        userProfile = userProfiles[0]
        self.assertEqual (up, userProfile, "The queried user profile was not equal")


    def test_creatingLab (self):
        u1 = User (username = "1234567s", password = "HelloWorld1", email = "1234567s@gmail.com")
        u1.save()
        u2 = User (username = "1234567t", password = "HelloWorld2", email = "1234567s@gmail.com")
        u2.save()
        up1 = UserProfile(user = u1)
        up1.save()
        up2 = UserProfile(user = u2)
        up2.save()

        course = Course (name = "CS2S", level = 5)
        course.save()

        lab = Lab (course = course, labNumber = 2)
        lab.save()

        lab.peopleInLab.add (up1)
        lab.peopleInLab.add (up2)

        lab.save()

        labs = Lab.objects.all()
        self.assertEqual (len(labs), 1, "Not only 1 lab was made")
        l = labs[0]
        self.assertEqual (lab, l, "The queried lab was not equal")


    def test_creatingPost (self):
        user = User (username = "1234567z", password = "HelloWorld1", email = "1234567s@gmail.com")
        user.save()
        author = UserProfile(user = user)
        author.save()

        course = Course (name = "CS2S", level = 5)
        course.save()
        lab = Lab (course = course, labNumber = 3)
        lab.save()

        content = "This is content"

        post = Post (author = author, postedIn = lab, content = content)
        post.save()

        posts = Post.objects.all()
        self.assertEqual (len(posts), 1, "Not only 1 post was made")
        p = posts[0]
        self.assertEqual (post, p, "The queried post was not equal")




class PopulationScriptTests (TestCase):
    def getCourseAndLabs (self):
        infoDict = {"name": "CS1P", "level": 1}

        addCourseAndLabs (infoDict)

        c = Course.objects.filter (name = infoDict["name"], level = infoDict["level"])

        return c


    def test_addCourseAndLabs_createsCategory (self):
        infoDict = {"name": "CS1P", "level": 1}

        addCourseAndLabs (infoDict)

        c = Course.objects.filter (name = infoDict["name"], level = infoDict["level"])

        self.assertEqual (len(c), 1)


    def test_addLabs_creates12LabsForCategory (self):
        infoDict = {"name": "CS1P", "level": 1}
        course = Course.objects.get_or_create (name = infoDict["name"], level = infoDict["level"])[0]

        addLabs (course)

        courseLabs = Lab.objects.filter (course = course)

        self.assertEqual (len(courseLabs), 12)


    def test_addPost_createsPost (self):
        course = Course.objects.get_or_create (name = "CS1P", level = 1)[0]
        course.save()

        lab = Lab.objects.get_or_create (labNumber = 4, course = course)[0]
        lab.save()

        user = User (username = "1234567s", password = "HelloWorld3")
        user.save()

        userProfile = UserProfile (user = user, name = "Patricia Bob")
        userProfile.save()

        infoDict = {"content" : "hello world", "timePosted" : datetime.now().replace(tzinfo=pytz.UTC), "attachedFile" : "populationScriptFiles/lab1Tips.txt", "name" : "Patricia Bob"}

        addPost (infoDict)

        labPosts = Post.objects.filter (postedIn = lab)

        self.assertEqual (len(labPosts), 1)


    def test_addUserAndProfile_createsFullUser (self):
        infoDict1 = {"username": "2281654m", "password": "HelloWorld1", "name": "Allan McGuire", "picture": "populationScriptFiles/coolAppa.jpg", "bio": "2nd year, Uni of Glasgow", "degree": "Computing Science", "email": "1234567m@student.gla.ac.uk"}
        infoDict2 = {"username": "11223344", "password": "HelloWorld6", "name": "Patricia Wallace", "email" : "patriciawallace@gmail.com", "degree" : "computing Science", "picture": "populationScriptFiles/tutorProfilePic.jpg", "bio": "i love to learn"}

        addUserAndProfile (infoDict1, "Student")
        addUserAndProfile (infoDict2, "Tutor")

        self.assertEqual (len(User.objects.all()), 2, "2 user objects were not created")
        self.assertEqual (len(UserProfile.objects.all()), 2, "2 profile objects were not created")


    def test_populate_createsAllNeededObjects (self):
        populate()

        self.assertEqual(len(User.objects.all()), 8, "Incorrect number of user made")
        self.assertEqual(len(UserProfile.objects.filter(status = "Student")), 5, "Incorrect number of students made")
        self.assertEqual(len(UserProfile.objects.filter(status = "Tutor")), 3, "Incorrect number of tutors made")
        self.assertEqual(len(Course.objects.all()), 7, "Incorrect number of courses made")
        self.assertEqual(len(Lab.objects.all()), 7*12, "Incorrect number of labs made")
        self.assertEqual(len(Post.objects.all()), 3, "Incorrect number of posts made")




class ViewTests (TestCase):

    


