from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.utils import timezone

from appLabShare.forms import *
from appLabShare.models import UserProfile, Course, Lab, Post


# The portal page that everyone should go to if they're not logged in
def enter (request):
    return render(request,"labShare/enter.html")



@login_required
def friendsList(request, username):
    contextDict = {}

    contextDict["pageUser"] = User.objects.get (username = username)
    contextDict["profile"] = UserProfile.objects.get (user = contextDict["pageUser"])

    return render(request, "labShare/friendsList.html", contextDict)



@login_required
def profile(request, username):
    contextDict = {}

    # Here I add the user object and user profile object of the page that the user is referring to
    # I call the user object 'pageUser' as if I used user this would be confused by the client user
    # in the template
    contextDict["pageUser"] = User.objects.get (username = username)
    contextDict["profile"] = UserProfile.objects.get (user = contextDict["pageUser"])

    return render(request, "labShare/profile.html", contextDict)



@login_required
def profileRedirect (request):
    # This will assign profile to None if the user did not make a profile
    try:
        profile = UserProfile.objects.get (user = request.user)
    except UserProfile.DoesNotExist:
        profile = None

    # If we got a profile then we know they did set up a profile
    # otherwise we redirect them to the the register-profile page
    if profile:
        return HttpResponseRedirect (reverse ("profile", args=[request.user.username]))
    else:
        return HttpResponseRedirect (reverse ("register-profile"))



@login_required
def labList(request, username):
    contextDict = {}

    contextDict["pageUser"] = User.objects.get (username = username)
    contextDict["profile"] = UserProfile.objects.get (user = contextDict["pageUser"])
    contextDict["labs"] = Lab.objects.filter(peopleInLab = contextDict["profile"])

    return render(request, "labShare/labList.html", contextDict)



@login_required
def lab (request, course, labNumber):
    contextDict = {}
    form = PostForm()

    user = request.user
    lab = Lab.objects.get (course = Course.objects.get (name = course), labNumber = labNumber)
    contextDict["lab"] = lab

    if not UserProfile.objects.get(user = user) in lab.peopleInLab.all():
        contextDict["error"] = "You are not enrolled in this lab!"
        return render(request, 'labShare/enrol.html', contextDict)
    else:
        contextDict["error"] = None


    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = UserProfile.objects.get(user=request.user)
            post.timePosted = timezone.now()
            post.postedIn = Lab.objects.get(labNumber = labNumber)
            post.save()
            return redirect('lab', course, labNumber)
    else:
        form = PostForm()

    contextDict["form"] = form
    contextDict["posts"] = Post.objects.filter(postedIn = lab).order_by('-timePosted')[:9]

    return render(request, 'labShare/lab.html', contextDict)



@login_required
def enrol (request):
    form = EnrolForm()
    contextDict = {}

    if (request.method == "POST"):
        form = EnrolForm (request.POST)

        # Getting the profile of the user to see whether they are a tutor or not
        profile = UserProfile.objects.get (user = request.user)

        if (form.is_valid()):
            # If the user is a student then they cannot create a lab and course and they can only be
            # enrolled in 1 lab per course, whereas a tutor can be in as many labs as they want
            # and can create labs and courses
            if (profile.status == "Student"):
                try:
                    course = Course.objects.get (name = form.cleaned_data["course"], level = form.cleaned_data["level"])
                    lab = Lab.objects.get (course = course, labNumber = form.cleaned_data["labNumber"])

                    if (request.POST.get ("enrol")):
                        if (course in profile.courses.all()):
                            labEnrolledIn = Lab.objects.get (course = course, peopleInLab = profile)
                            labEnrolledIn.peopleInLab.remove (profile)
                        else:
                            profile.courses.add (course)

                        lab.peopleInLab.add (profile)
                    else:
                        lab.peopleInLab.remove (profile)
                        profile.courses.remove (course)

                    return redirect ('labList', request.user.username)

                # Trying to get it so that if the course exists, but the level isn't correct, display the correct error message
                # except Course.level.DoesNotExist:
                #     contextDict["error"] = "The course exists, but you have not entered the correct level"
                except Course.DoesNotExist:
                    contextDict["error"] = "The course does not exist"
                except Lab.DoesNotExist:
                    contextDict["error"] = "The lab does not exist"
            else:
                try:
                    if (request.POST.get ("enrol")):
                        course = Course.objects.get_or_create (name = form.cleaned_data["course"], level = form.cleaned_data["level"])[0]
                        lab = Lab.objects.get_or_create (course = course, labNumber = form.cleaned_data["labNumber"])[0]

                        profile.courses.add (course)
                        lab.peopleInLab.add (profile)
                    else:
                        course = Course.objects.get (name = form.cleaned_data["course"], level = form.cleaned_data["level"])
                        lab = Lab.objects.get (course = course, labNumber = form.cleaned_data["labNumber"])

                        lab.peopleInLab.remove (profile)

                        if not Lab.objects.get (peopleInLab = profile, course = course):
                            profile.courses.remove (course)

                except Course.DoesNotExist:
                    contextDict["error"] = "The course does not exist"
                except Lab.DoesNotExist:
                    contextDict["error"] = "The lab does not exist"

                course.save()
                lab.save()

                return redirect ('labList', request.user.username)


    contextDict["form"] = form
    courseList = Course.objects.order_by("level", "name")
    labList = []

    # I zip the course and their labs together here so I can easily access and iterate through them
    # in the template
    for course in courseList:
        labList.append(Lab.objects.filter(course = course).order_by("labNumber"))

    contextDict["table"] = zip(courseList, labList)

    return render (request, "labShare/enrol.html", contextDict)



@login_required
def register_profile (request):
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm (request.POST, request.FILES)

        if form.is_valid():
            userProfile = form.save (commit = False)
            userProfile.user = request.user
            userProfile.save()
            # Once the user has registered fully, go to profile page
            # as signup automatically logs in once complete.
            return redirect ("profileRedirect")
        else:
            print (form.errors)

    contextDict = {"form": form}

    return render (request, "labShare/setup_profile.html", contextDict)



@login_required
def editProfile(request):
    profile = UserProfile.objects.get (user = request.user)
    form = UserProfileForm(instance = profile)
    contextDict = {}

    if request.method == 'POST':
        form = UserProfileForm(instance = profile, data = request.POST, files = request.FILES)
        if form.is_valid():
            userProfile = form.save(commit = False)
            userProfile.save()
            return redirect("profileRedirect")
        else:
            print (form.errors)

    contextDict = {"form": form}
    contextDict["profile"] = UserProfile.objects.get (user = request.user)

    return render(request, "registration/edit_profile.html", contextDict)



@login_required
def addFriend (request):
    contextDict = {}

    form = AddFriendForm()

    if (request.method == "POST"):
        form = AddFriendForm (request.POST)

        if (form.is_valid()):
            user = UserProfile.objects.get (user = request.user)
            try:
                friend = UserProfile.objects.get (user = User.objects.get (username = form.cleaned_data["friend"]))

                if (request.POST.get ("AddFriend")):
                    user.friends.add (friend)
                else:
                    user.friends.remove (friend)

                return redirect ("friendsList", request.user.username)
            except User.DoesNotExist:
                contextDict["error"] = "The user you entered does not exist!"


    contextDict["form"] = form

    return render (request, "labShare/addFriend.html", contextDict)


# Just a reminder that a lot of the user related views (e.g. login, registration etc.)
# are dealt with the django-registration-redux package and so you should look there for those views
