# Twitter Display
## Bea Casey, Nick Caravias, Justin Schaumberger and Andrew Lee

For our CSCI479 senior design culminating project, we are creating a webpage that will display Tweets to the computer science community at Bucknell. Certain professors who wish to have certain Tweets shown will be displayed on the board if they use a hashtag, and other accounts such as ACM, ACM-W, and IEEE will be displayed. The website features a slow automatic scroll and automatically pulls new Tweets everyday.   
 
The project utilizes the Tweepy API to extract Tweets from Twitter and then generate HTML representations of the Tweets. This iformation is stored on a Postgres Database and displayed on Heroku using the Django framework. In addition to the Tweets, the website also has a notification board to allow student organizations and professors to post upcoming events or research and job opportunities. 

The webpage can be viewed on the screen behind the CS student space on the 3rd floor of Dana Engineering. 


*How to add new accounts*
Within the GitHub repository, there is a CSV file called “accounts.csv” (located at hello/accounts.csv). This file contains a list of all the Twitter accounts that should be checked for new Tweets. The first column specifies the Twitter accounts’ username while the second column denotes if the user only wants Tweets posted with the hashtag “BucknellCSNews”. If the value in the second column is 1, the only Tweets pulled from the account will be those with the given hashtag. Otherwise if there is a 0, all Tweets will be pulled. To update the list of accounts to be pulled, simply update this file with new Twitter accounts and push the code repository to Heroku.  


