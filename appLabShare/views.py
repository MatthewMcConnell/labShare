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


# def labList(request, username):
#     contextDict = {}
#
#     contextDict["pageUser"] = User.objects.get (username = username)
#     contextDict["profile"] = UserProfile.objects.get (user = contextDict["pageUser"])
#
#     return render(request, "labShare/labList.html", contextDict)
#
# # Don't delete the comment below, just altered this so I can test the page
# #def lab(request, course, labNumber):
# def lab(request):
#     # This will be the template view for the specific lab page, not currently finished.
#     return render(request, "labShare/lab.html")

@login_required
def post_list(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = UserProfile.objects.get(user=request.user)
            post.timePosted = timezone.now()
            post.postedIn = Lab.objects.get(labNumber = 8)
            post.save()
            return redirect('lab_posts')
    else:
        form = PostForm()

    posts = Post.objects.order_by('-timePosted')[:9]
    contextDict = {'form':form, 'posts':posts}

    return render(request, 'labShare/lab_posts.html', contextDict)


############# WORK IN PROGRESS #############
def enrol (request):
    form = EnrolForm()
    contextDict = {}

    if (request.method == "POST"):
        form = EnrolForm (request.POST)

        # Getting the profile of the user to get whether they are a tutor or not
        profile = UserProfile.objects.get (user = request.user)


        if (form.is_valid()):
            if (profile.status == "Student"):
                try:
                    course = Course.objects.get (name = form.cleaned_data["course"], level = form.cleaned_data["level"])
                    lab = Lab.objects.get (course = course, labNumber = form.cleaned_data["labNumber"])

                    lab.peopleInLab.add (profile)

                    course.save()
                    lab.save()

                    return redirect ('labList', request.user.username)

                except Course.DoesNotExist:
                    contextDict["error"] = "The course does not exist"
                except Lab.DoesNotExist:
                    contextDict["error"] = "The lab does not exist"
            else:
                course = Course.objects.get_or_create (name = form.cleaned_data["course"], level = form.cleaned_data["level"])[0]
                lab = Lab.objects.get_or_create (course = course, labNumber = form.cleaned_data["labNumber"])[0]

                lab.peopleInLab.add (profile)

                course.save()
                lab.save()

                return redirect ('labList', request.user.username)



    contextDict["form"] = form

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
def user_edit(request, username):
    profile = UserProfile.objects.get (user = request.user)
    form = UserProfileForm(instance = profile)

    if request.method == 'POST':
        form = UserProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("profileRedirect")

    return render(request, "registration/edit_profile.html", {'form':form})


# Just a reminder that a lot of the user related views (e.g. login, registration etc.)
# are dealt with the django-registration-redux package and so you should look there for those views
