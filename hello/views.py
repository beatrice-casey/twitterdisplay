from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEPxTgEAAAAAqnem0D0Cf8c1zRJ1AgKrN6wiHRI%3DfHNJuInuMppQGzaicMdr4ds7hfOlHNySVwrdrNRvECFMm6bFE1'
consumer_key = "dFGI5f6OBN0QfprVQZmBhA40r"
consumer_secret = "K5dvFQ2h9T1mXvOzrhS1why4COACEUuUssSJZryajWZS0mB1Ho"
access_token = "1436417414728663041-ypu8oIwt1oArCgwsPolWqSjnSnJX5R"
access_token_secret = "IMwmI0nIWGMeCbdeEEJwEn3a6WnPVDaC2sfXfiHGa5ZFX"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


def build_account_list():
    # account_list = []
    # # extract users from txt file
    # file = open('users.txt', 'r')
    # count = 0
    # while True:
    #     count += 1

    #     # Get next line from file
    #     line = file.readline().strip()

    #     # if line is empty
    #     # end of file is reached
    #     if not line:
    #         break
    #     account_list.append(line)
    #     # print("Line{}: {}".format(count, line.strip()))
    # file.close()

    account_list = ["TheOfficialACM", "Bucknell_Bison"]

    return account_list


def run():

    # build the list of users to extract
    account_list = build_account_list()
    # connect to the API
    api = tweepy.API(auth)
    d = dict()
    # go through each user
    for account in account_list:
        d[account] = []
        print("Getting data for " + account)
        # get the tweetss
        statuses = api.user_timeline(screen_name=account, count=3, trim_user=True, exclude_replies=True)
        # loop through the tweets
        for status in statuses:
            d[account].append(status._json)
