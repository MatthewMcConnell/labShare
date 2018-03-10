from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from appLabShare.forms import UserProfileForm
from appLabShare.models import UserProfile
from django.contrib.auth.models import User


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
    return HttpResponseRedirect (reverse ("profile", args=[request.user.username]))


def labList(request, username):
    # Perhaps here we need to obtain the username (i.e. the student/staff id) to pass as a context dict
    return render(request, "labShare/labList.html")


def lab(request, course, labNumber):
    # This will be the template view for the specific lab page, not currently finished.
    return render(request, "labShare/lab.html")


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
