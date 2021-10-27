from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Greeting, Tweet

# Create your views here.

def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}

    context["dataset"] = Tweet.objects.all()

    return render(request, "index.html", context)


def api_response(request):
    pass


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
