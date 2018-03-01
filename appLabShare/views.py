from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from appLabShare.forms import UserProfileForm

def testView (request):
    return HttpResponse("The page worked!")

def login(request):
    return render(request, "registration/login.html")

def signUp(request):
    return render(request, "labshare/signup.html")


@login_required
def register_profile (request):
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm (request.POST, request.FILES)

        if form.is_valid():
            userProfile = form.save (commit = False)
            userProfile.user = request.user
            userProfile.save()

            return redirect ("login")
        else:
            print (form.errors)

    contextDict = {"form": form}

    return render (request, "labShare/profile_registration.html", contextDict)


