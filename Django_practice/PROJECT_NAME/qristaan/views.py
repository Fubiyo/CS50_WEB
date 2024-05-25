from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "hello/index.html")

def qristaan(request):
    return HttpResponse("sup q")

def greet(request, namae):
    return render(request, "hello/index.html", {
        "name": namae.capitalize()
    })
