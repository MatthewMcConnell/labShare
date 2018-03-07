from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from appLabShare.forms import UserProfileForm

def testView (request):
    return HttpResponse("The page worked!")

def enter (request):
    return render(request,"labShare/enter.html")

def login(request):
    return render(request, "registration/login.html")

def signUp(request):
    return render(request, "labshare/signup.html")

def profile(request):
    return render(request, "labshare/profile.html")


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
            return redirect ("profile")
        else:
            print (form.errors)

    contextDict = {"form": form}

    return render (request, "labShare/setup_profile.html", contextDict)
