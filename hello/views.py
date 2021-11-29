from urllib.parse import urlencode

import requests
import tweepy
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from tweepy import API, OAuthHandler
from hello.models import Tweet, Username
import schedule
import time
import csv
import datetime
import psycopg2
import os

# CONSTANTS
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEPxTgEAAAAAqnem0D0Cf8c1zRJ1AgKrN6wiHRI%3DfHNJuInuMppQGzaicMdr4ds7hfOlHNySVwrdrNRvECFMm6bFE1'
CONSUMER_KEY = "dFGI5f6OBN0QfprVQZmBhA40r"
CONSUMER_SECRET = "K5dvFQ2h9T1mXvOzrhS1why4COACEUuUssSJZryajWZS0mB1Ho"
ACCESS_TOKEN = "1436417414728663041-ypu8oIwt1oArCgwsPolWqSjnSnJX5R"
ACCESS_TOKEN_SECRET = "IMwmI0nIWGMeCbdeEEJwEn3a6WnPVDaC2sfXfiHGa5ZFX"

# the hashtag that needs to be included for certain accounts
HASHTAG = "BucknellCSNews"

# GLOBAL VARIABLES
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

cursor = None
conn = None


def index(request):
    """
    Renders the HTML format to update the web page
    :param request: the request being made
    :return: the rendered HTML template
    """
    global cursor,conn
    
    if cursor is None:
        cursor, conn = start_pgsql()

    add_to_db(cursor, conn)

    # get data from pgsql
    tweets = Tweet.objects.all()

    # html = get_from_db(cursor)
    # TODO HAS to be a dictionary

    return render(request, "index.html", {'tweets': tweets})


def start_pgsql():
    """
    Creates a connection to the Postgres DB
    :return: the cursor and connection to the Postgres DB 
    """
    enginge = 'django.db.backends.postgresql_psycopg2'
    name = 'ddtqls08im6ebr'
    user = 'hrkyzevdhovtsu'
    password = '3a05d690de5bdcf66b0580f305a103b059ff4f5544fcde88aa193f496db11421'
    host = 'ec2-3-226-165-74.compute-1.amazonaws.com'
    port = 5432

    db_conn = psycopg2.connect(
        dbname=name,
        user=user,
        password=password,
        host=host,
        port=port
    )

    db_cursor = conn.cursor()
    return db_cursor, db_conn


def add_to_db(cursor, conn):

    usernames, html, dates = run()
    size = cursor.execute("SELECT count(*) FROM hello_tweet")
    if size == 50:
        delete_from_db(cursor, len(usernames)) 
  
    for i in range(len(html)):
        cursor.execute("INSERT INTO hello_tweet (username, date, html) VALUES(%s, %s, %s)", (usernames[i], dates[i], html[i]))
    

    conn.commit()

    # cursor.fetchall()


def get_from_db(cursor):
    cursor.execute(f'SELECT * from hello_tweet')
    data = cursor.fetchall()

    return data[1]

def delete_from_db(cursor, num_to_delete):

    for i in range(num_to_delete):
        cursor.execute('DELETE FROM hello_tweet WHERE id = (row_to_delete) VALUES(%s)', (i))




def build_account_list():
    """
    Builds a list of account to extract Tweets from
    :return: a list of tuples containing the username of the account and whether they are hashtag only
    """
    account_list = []
    # Open the file containing the accounts to scrape from
    with open("./hello/accounts.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # Skip the header of the CSV
            if line_count == 0:
                line_count += 1
                continue
            else:
                account_list.append((row[0], row[1]))
                line_count += 1

    return account_list


def generate_html(url: str) -> str :
    """
    Generates the HTML for a given Tweet
    :param url: The URL for a given Tweet
    :return: the HTML display for a given Tweets
    """
    query_string = urlencode({'url': url})  # 'omit_script': 1
    oembed_url = f"https://publish.twitter.com/oembed?{query_string}"

    r = requests.get(oembed_url)

    if r.status_code == 200:
        result = r.json()
        return result['html'].strip()
    return ""


def run() -> Tuple[[str], [str],[str]]:
    """
    Pulls Tweets from Twitter
    :return: a list of usernames, Tweet HTMLs, and dates for the pulled Tweets 
    """
    account_list = build_account_list()
    dates = []
    users = []
    htmls = []

    prev_date = datetime.datetime.now() - datetime.timedelta(days=1)

    # go through each user
    for account_entry in account_list:

        try:
            account = account_entry[0]
            isHashtagOnly = int(account_entry[1]) == 1
            print("Getting data for " + account)
            # get the tweets
            tweets = api.user_timeline(screen_name=account, trim_user=True,
                                   exclude_replies=True, )

            for tweet in tweets:
                d = tweet._json['created_at'].split(' ')
                tweet_date = datetime.datetime(year=int(d[-1]), month=int(get_month(d[1])),
                                           day=int(d[2]))  # Time, without a date

                # keep looping until encounter tweet with date past 1 day ago (since last update)
                if tweet_date < prev_date:
                    break

                # obtain the tweet url from the json request

                url = "https://twitter.com/" + account + "/status/" + tweet._json['id_str']
                html = generate_html(url)

                if html != "":
                    # Working with hashtags
                    hashtags = []
                    for entry in tweet._json['entities']['hashtags']:
                        hashtags.append(entry['text'])

                    # Put in DB
                    if not isHashtagOnly or HASHTAG in hashtags:

                        # date = generateDate(tweet)
                        time = tweet._json['created_at'].split(' ')
                        month = time[1]
                        day = time[2]
                        year = time[-1]
                        date = datetime.datetime(month=get_month(month), day=int(day), year=int(year))

                        # find the spot in the list to put the new Tweet
                        index = 0
                        while index < len(dates):
                            if dates[index] < date:
                                break
                            index += 1

                        htmls.insert(index, html)
                        dates.insert(index, date)
                        users.insert(index, account)

                else:
                    print("Not able to get Tweet for " + account)
        except:
            continue

    for index in range(len(dates)):
        dates[index] = str(dates[index])
    return users, htmls, dates




def generateDate(status:str) -> str :
    """
    Generates the date for a given Tweet requests
    :param status: the request from a Tweet
    :return: the date of the Tweet as a String in day/month/year format
    """
    time_created_at = (status._json['created_at']).split(" ")
    month = time_created_at[1]
    day = time_created_at[2]
    year = time_created_at[-1]
    month = get_month(month)
    date = day + "/" + str(month) + "/" + year
    return date


def get_month(month: str) -> int:
    """
    Converts abbreviation of the month to the number of the month
    :param month: String abbreviation for a month
    :return: The number of the month
    """
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
    return month
