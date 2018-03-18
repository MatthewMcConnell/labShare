from django.test import TestCase
from django.core.urlresolvers import reverse

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
    # HELPER METHODS #

    def create_user (self, username, password, name):
        user = User.objects.get_or_create (username = username, password = password)[0]
        user.set_password (user.password)
        user.save()

        userProfile = UserProfile.objects.get_or_create (user = user, name = name)[0]
        userProfile.save()

        return user, userProfile, {"username": username, "password": password}


    def loginUser (self, userDict):
        self.client.post (reverse ("auth_login"), userDict)


    # ENTER VIEW #

    def test_enter_page_has_link_to_login (self):
        try:
            response = self.client.get (reverse ("enter"))
        except:
            return False

        self.assertIn (reverse ("auth_login"), response.content.decode ("ascii"))


    # LOGIN VIEW #

    def test_login_shows_go_to_profile_link_when_already_logged_in (self):
        user, userProfile, userDict = self.create_user ("1234567s", "HelloWorld1", "Matt")

        try:
            # login
            self.loginUser (userDict)

            # Getting the login page again
            response = self.client.get (reverse ("auth_login"))
        except:
            return False

        self.assertIn (reverse ("profileRedirect"), response.content.decode('ascii'))


    # PROFILE REDIRECT VIEW #

    def test_profileRedirect_redirects_to_profileSetup_when_user_does_not_have_profile (self):
        try:
            user = User.objects.get_or_create (username = "1234567s", password = "HelloWorld1")
            user.set_password (user.password)
            user.save()

            self.loginUser ({"username": "1234567s", "password": "HelloWorld1"})

            response = self.client.get (reverse ("profileRedirect"))
        except:
            return False

        self.assertRedirects (response, reverse ("register-profile"))


    def test_profileRedirect_redirects_to_profile_when_user_has_profile (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("profileRedirect"))
        except:
            return False
        
        self.assertRedirects (response, reverse ("profile", args=["1234567s"]))


    # SIGN OUT VIEW #

    def test_signOut_redirects_to_enter_page (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("auth_logout"))
        except:
            return False

        self.assertRedirects (response, reverse ("enter"))


    # PROFILE VIEW #

    def test_profile_page_has_nav_links (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("profile"))

            cdResponse = response.content.decode ("ascii")
        except:
            return False

        self.assertIn (reverse ("profile" ,"1234567s"), cdResponse, "There was no my profile link")
        self.assertIn (reverse ("labList", "1234567s"), cdResponse, "There was no my labs link")
        self.assertIn (reverse ("friendsList", "1234567s"), cdResponse, "There was no my friends link")
        self.assertIn (reverse ("auth_logout"), cdResponse, "There was no sign out link")


    def test_profile_shows_edit_profile_when_user_is_viewing_own_profile (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("profile", "1234567s"))
        except:
            return False

        self.assertIn (reverse ("edit_profile"), response.content.decode ("ascii"))


    def test_profile_does_not_show_edit_profile_when_user_is_viewing_others_profile (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            self.create_user ("1234567t", "HelloWorld1", "Matt")

            response = self.client.get (reverse ("profile", "1234567t"))
        except:
            return False

        self.assertNotIn (reverse ("edit_profile"), response.content.decode ("ascii"))



    # FRIENDS LIST VIEW #

    def test_friendsList_shows_friends (self):
        try:
            user, userProfile, userDict = self.create_user ("1234567s", "HelloWorld1", "Matt")

            self.loginUser (userDict)

            userProfile.friends.add (self.create_user ("1234567t", "HelloWorld1", "Matty")[1])

            response = self.client.get (reverse ("friendsList", "1234567s"))
        except:
            return False

        self.assertIn ("1234567t", response.content.decode ("ascii"))


    def test_friendsList_shows_noFriendsMessage (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("friendsList", "1234567s"))
        except:
            return False

        self.assertIn ("This user has no friends!".lower(), response.content.decode ("ascii").lower())


    def test_friendsList_shows_add_link_when_user_is_viewing_their_own_friendsList (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("friendsList", "1234567s"))
        except:
            return False

        self.assertIn (reverse ("addFriend"), response.content.decode ("ascii"))


    def test_friendsList_does_not_show_add_link_when_user_is_viewing_others_friendsList (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            self.create_user ("1234567t", "HelloWorld1", "Matt")

            response = self.client.get (reverse ("friendsList", "1234567t"))
        except:
            return False

        self.assertNotIn (reverse ("addFriend"), response.content.decode ("ascii"))


    # LAB LIST VIEW #

    def test_labList_shows_noLabsMessage (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("labList", "1234567s"))
        except:
            return False

        self.assertIn ("This user is not enrolled in any labs!".lower(), response.content.decode ("ascii").lower())
            

    def test_labList_shows_labs_enrolled_in (self):
        try:
            user, userProfile, userDict = self.create_user ("1234567s", "HelloWorld1", "Matt")

            self.loginUser (userDict)

            course = Course.objects.get_or_create (name = "CS1CT", level = 1)
            lab = Lab.objects.get_or_create (course = course, labNumber = 1)
            lab.peopleInLab.add (userProfile)

            response = self.client.get (reverse ("labList", "1234567s"))
        except:
            return False

        self.assertIn ("CS1CT - 1", response.content.decode ("ascii"))


    def test_labList_shows_enrol_link_when_user_is_viewing_their_own_labList (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            response = self.client.get (reverse ("labList", "1234567s"))
        except:
            return False

        self.assertIn (reverse ("enrol"), response.content.decode ("ascii"))


    def test_labList_does_not_show_enrol_link_when_user_is_viewing_others_labList (self):
        try:
            self.loginUser (self.create_user ("1234567s", "HelloWorld1", "Matt")[2])

            self.create_user ("1234567t", "HelloWorld1", "Matt")

            response = self.client.get (reverse ("labList", "1234567t"))
        except:
            return False

        self.assertNotIn (reverse ("enrol"), response.content.decode ("ascii"))


    






