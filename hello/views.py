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

    account_list = ["BucknellCS"]

    return account_list

# Makes a request to get the html for a given Tweet URL
def generate_html(url):
    query_string = urlencode({'url': url}) # 'omit_script': 1
    oembed_url = f"https://publish.twitter.com/oembed?{query_string}"

    r = requests.get(oembed_url)

    if r.status_code == 200:
        result = r.json()
        return result['html'].strip()
    return ""

def run():
    # build the list of users to extract
    account_list = build_account_list()

    # go through each user
    for account in account_list:
        try:

            print("Getting data for " + account)
            # get the tweetss
            statuses = api.user_timeline(screen_name=account, count=10, trim_user=True, exclude_replies=True)
            # loop through the tweets
            for status in statuses:
                # obtain the tweet url from the json request
                url = "https://twitter.com/" + account + "/status/" + status._json['id_str']
                html = generate_html(url)
                # print(status._json.keys())
                if html != "":
                    # time_created_at = time the Tweet was made
                    # account = username of the account
                    # html = the html to embed the Tweet
                    date = generateDate(status)

                    # print(status._json['text'])

                    # Working with hashtags
                    hashtags = []
                    for entry in status._json['entities']['hashtags']:
                        hashtags.append(entry['text'])
                    # print(hashtags)

                    # print(html)
                else:
                    print("Not able to get Tweet for " + account)
        except:
            continue


def generateDate(status):
    time_created_at = (status._json['created_at']).split(" ")
    month = time_created_at[1]
    day = time_created_at[2]
    year = time_created_at[-1]
    if month == "Jan":
        month = 1
    elif month == "Feb":
        month = 2
    elif month == "Mar":
        month = 3
    elif month == "Apr":
        month = 4
    elif month == "May":
        month = 5
    elif month == "Jun":
        month = 6
    elif month == "Jul":
        month = 7
    elif month == "Aug":
        month = 8
    elif month == "Sept":
        month = 9
    elif month == "Oct":
        month = 10
    elif month == "Nov":
        month = 11
    elif month == "Dec":
        month = 12
    date = day + "/" + str(month) + "/" + year
    return date    
