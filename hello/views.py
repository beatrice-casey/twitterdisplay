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

# the hashtag that needs to be included for certain accounts
HASHTAG = "BucknellCSNews"
# the number of tweets to pull from each user
TWEETS_PER_USER = 10

# GLOBAL VARIABLES
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)



def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def build_account_list():
    # comment
    account_list = []
    # # extract users from txt file
    with open("accounts.csv",'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                continue
            else:
                account_list.append((row[0],row[1]))
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
    



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

    users = []
    htmls =[]
    dates = []


    # go through each user
    for account_entry in account_list:
        try:
            account = account_entry[0]
            isHashtagOnly = account[1] == 1
            #print("Getting data for " + account)
            # get the tweetss
            statuses = api.user_timeline(screen_name=account, count=TWEETS_PER_USER, trim_user=True, exclude_replies=True)
            # loop through the tweets
            for status in statuses:
                # obtain the tweet url from the json request
                url = "https://twitter.com/" + account + "/status/" + status._json['id_str']
                html = generate_html(url)
                if html != "":
                    # Working with hashtags
                    hashtags = []
                    for entry in status._json['entities']['hashtags']:
                        hashtags.append(entry['text'])

                    # Put in DB
                    if(not isHashtagOnly or HASHTAG in hashtags):
                        # time_created_at = time the Tweet was made
                        # account = username of the account
                        # html = the html to embed the Tweet
                        date = generateDate(status)
                        users.append(account)
                        htmls.append(html)
                        dates.append(date)
                else:
                    print("Not able to get Tweet for " + account)
        except:
            continue

    return users,htmls,dates


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


            

# for testing purposes (to run just the single file)
run()
