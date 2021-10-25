from urllib.parse import urlencode

import requests
import tweepy
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from tweepy import API, OAuthHandler

# CONSTANTS
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEPxTgEAAAAAqnem0D0Cf8c1zRJ1AgKrN6wiHRI%3DfHNJuInuMppQGzaicMdr4ds7hfOlHNySVwrdrNRvECFMm6bFE1'
CONSUMER_KEY = "dFGI5f6OBN0QfprVQZmBhA40r"
CONSUMER_SECRET = "K5dvFQ2h9T1mXvOzrhS1why4COACEUuUssSJZryajWZS0mB1Ho"
ACCESS_TOKEN = "1436417414728663041-ypu8oIwt1oArCgwsPolWqSjnSnJX5R"
ACCESS_TOKEN_SECRET = "IMwmI0nIWGMeCbdeEEJwEn3a6WnPVDaC2sfXfiHGa5ZFX"

# GLOBAL VARIABLES
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
# I don't think this is needed (-Justin)
#auth_api = API(auth)



def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


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
            statuses = api.user_timeline(screen_name=account, count=3, trim_user=True, exclude_replies=True)
            # loop through the tweets
            for status in statuses:
                # obtain the tweet url from the json request
                url = "https://twitter.com/"+account+"/status/"+status._json['id_str']
                html = generate_html(url)
                #print(status._json.keys())
                if(html != ""):
                    # time_created_at = time the Tweet was made
                    # account = username of the account
                    # html = the html to embed the Tweet
                    time_created_at = status._json['created_at']
                    #print(html)
                else:
                    print("Not able to get Tweet for "+account)
        except:
            continue


            

# for testing purposes (to run just the single file)
run()
