from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from appLabShare.forms import UserProfileForm


# The portal page that everyone should go to if they're not logged in
# If they are logged in then shouldn't we just redirect them to their profile straight away?
def enter (request):
    return render(request,"labShare/enter.html")

# def login(request):
#     return render(request, "registration/login.html")

# def signUp(request):
#     return render(request, "labShare/signup.html")

@login_required
def profile(request):
    # Perhaps here we need to obtain the username (i.e. the student/staff id) to pass as a context dict
    return render(request, "labShare/profile.html")


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



# Just a reminder that a lot of the user related views (e.g. login, registration etc.)
# are dealt with the django-registration-redux package and so you should look there for those views