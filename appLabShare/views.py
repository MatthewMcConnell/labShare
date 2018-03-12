from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User

from appLabShare.forms import UserProfileForm, EnrolForm
from appLabShare.models import UserProfile, Course, Lab


# The portal page that everyone should go to if they're not logged in
# If they are logged in then shouldn't we just redirect them to their profile straight away?
def enter (request):
    return render(request,"labShare/enter.html")

# def login(request):
#     return render(request, "registration/login.html")

# def signUp(request):
#     return render(request, "labShare/signup.html")


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
    # The code below will assign profile to None if the user did not make a profile
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


def labList(request, username):
    contextDict = {}

    contextDict["pageUser"] = User.objects.get (username = username)
    contextDict["profile"] = UserProfile.objects.get (user = contextDict["pageUser"])

    return render(request, "labShare/labList.html", contextDict)


def lab(request, course, labNumber):
    # This will be the template view for the specific lab page, not currently finished.
    return render(request, "labShare/lab.html")



############# WORK IN PROGRESS #############
def enrol (request):
    form = EnrolForm()

    if (request.method == "POST"):
        form = EnrolForm (request.POST)

        # Getting the profile of the user to get whether they are a tutor or not
        profile = UserProfile.objects.get (user = request.user)

        # Here I am storing the function as a first class object so that it is used
        # depending on whether the person is a tutor or not
        if (profile.isStudent):
            courseFn = Course.objects.get ()
            labFn = Lab.objects.get ()
        else:
            courseFn = Course.objects.get_or_create ()
            labFn = Lab.objects.get_or_create ()


        if (form.is_valid()):
            course = courseFn (name = form.cleaned_data["course"], level = form.cleaned_data["level"])
            lab = labFn (course = course, labNumber = form.cleaned_data["labNumber"])

            lab.peopleInLab.add (profile)

            course.save()
            lab.save()

            return HttpResponse ("You enrolled!")


    contextDict = {"form": form}

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



# Just a reminder that a lot of the user related views (e.g. login, registration etc.)
# are dealt with the django-registration-redux package and so you should look there for those views
