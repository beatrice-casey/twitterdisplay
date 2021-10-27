from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Tweet, User

# Create your views here.
def index(request):
    # create to store database contents
    context = {}

    # select from SQLite
    context["dataset"] = Tweet.objects.all()
   
    return render(request, "index.html", context)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
