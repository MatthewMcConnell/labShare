from django.shortcuts import render
from django.http import HttpResponse

def testView (request):
    return HttpResponse("The page worked!")

def index(request):
    return render(request, "labShare/index.html")
    
def signUp(request):
    return render(request, "labshare/signup.html")
