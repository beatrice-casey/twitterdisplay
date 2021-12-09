# Bucknell Twitter Display

For our CSCI479 senior design culminating project, we are creating a webpage that will display Tweets to the computer science community at Bucknell. Certain professors who wish to have certain Tweets shown will be displayed on the board if they use a hashtag, and other accounts such as ACM, ACM-W, and IEEE will be displayed. The website features a slow automatic scroll and automatically pulls new Tweets everyday. In addition to the scrolling Twitter feed, the webpage also has a notification board. The board is updated as users fill out a Google Form with specific Bucknell related events or notifications.   

![Screen Shot 2021-12-09 at 5 47 38 PM](https://user-images.githubusercontent.com/44034523/145487984-e937b249-fa27-4f75-b642-b1e79140c9b6.jpeg) 
 


The webpage can be viewed on the screen behind the CS student space on the 3rd floor of Dana Engineering.  


## Tweet Collection
The project utilizes the [Tweepy API](https://github.com/tweepy/tweepy) to extract Tweets from Twitter and then generate HTML representations of the Tweets. This information is stored on a Postgres Database and displayed on Heroku using the Django framework. The Tweets are pulled every 24 hours and the program only collects Tweets that have been published since the last pull. The web page automatically refreshes every 24hrs via a [chrome extension](https://chrome.google.com/webstore/detail/page-refresh/hmooaemjmediafeacjplpbpenjnpcneg?hl=en). This triggers the pulling of new Tweets and the refresh of the front ennd. 



## Event Board
In addition to the Tweets, the website also has a notification board to allow student organizations and professors to post upcoming events or research and job opportunities. There is a QR code on the website that will redirect users to a Google Form. Once the form is submitted, the information will be populated to the table on the webpage upon the next refresh. 




## How to Use



### Adding New Twitter Accounts

The project utilizes the Tweepy API to extract Tweets from Twitter and then generate HTML representations of the Tweets. This information is stored on a Postgres Database and displayed on Heroku using the Django framework. In addition to the Tweets, the website also has a notification board to allow student organizations and professors to post upcoming events or research and job opportunities. 




## Contributing
The repository is built in such a way that the project is self-sufficient and should be able to be maintained without the need for constant updates. 

In the event that the accounts being pulled from needs to be modified there is a CSV file within the GitHub repository called “accounts.csv” (located at hello/accounts.csv). This file contains a list of all the Twitter accounts that should be checked for new Tweets. The first column specifies the Twitter accounts’ username while the second column denotes if the user only wants Tweets posted with the hashtag “BucknellCSNews”. If the value in the second column is 1, the only Tweets pulled from the account will be those with the given hashtag. Otherwise if there is a 0, all Tweets will be pulled. To update the list of accounts to be pulled, simply update this file with new Twitter accounts and push the code repository to Heroku. 

## Authors
Bea Casey, Nick Caravias, Justin Schaumberger and Andrew Lee 

