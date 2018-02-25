from django.shortcuts import render
from django.http import HttpResponse

def testView (request):
    return HttpResponse ("The page worked!")