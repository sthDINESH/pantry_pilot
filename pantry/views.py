from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def pantry_list(request):
    return HttpResponse("This will list pantry items")
