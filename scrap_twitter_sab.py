"""
coding:utf-8
SPRING 2022 -CIS 493/593 – BIG DATA LAB ASSIGNMENT - 3
Semi-Structured Data Processing with NoSQL Database Server MongoDB
Collecting Social Media Data from Twitter Real-time Data Stream and
Storing and Retrieving to Process from a Semi-Structured Database Server MongoDB
credits: https://python.plainenglish.io/scraping-tweets-with-tweepy-python-59413046e788
Author: Sabareeswaran Shanmugam
•	Scripting language – python 3.7
•	Database –MongoDB 5.0.6 Compass , Text analysis : Pandas dataframe
•	IDE - PyCharm 2021.3.1 (Professional Edition)
    Runtime version: 11.0.13+7-b1751.21 x86_64
    VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
    macOS 12.1
    Memory: 2048M
    Cores: 16

This part :Scraping twitter data and store it as a Semi-Structured Data.
"""

import tweepy
from tweepy import OAuthHandler
import jsonpickle
import configparser
import os
import time
import csv

# setting Absolute Path
sab_absolute_path = os.path.dirname(os.path.abspath(__file__))

# Authenticating Twitter API
# read configs
config = configparser.ConfigParser()
config.read(sab_absolute_path +'/config.ini')
api_key = config['twittersabareeswaran']['api_key']
api_key_secret = config['twittersabareeswaran']['api_key_secret']
access_token = config['twittersabareeswaran']['access_token']
access_token_secret = config['twittersabareeswaran']['access_token_secret']

# Pass My twitter credentials to tweepy via its OAuthHandler (V1 and V2 Supported)
auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## Automating scraping twitter API V2 using tweepy Python Package.

# Topic : Ukrainewar related tags.
# Calling API every 15 minutes to prevent Twitter Api limits( 900 requests / 15 Min # PER USER - Elevated Access)

def scraptwitter_tweets_sab(search_words, date_since, numTweets, numRuns):
    # Scraped data is stored as Json file and then loaded into local Mongodb.
    # Collect tweets using the Cursor object
    with open(sab_absolute_path +"/twitter_data/UkraineRussiaWar6000_Tweets.json", 'w') as filename,open(sab_absolute_path+ "/twitter_data/UkraineTextData6k_Sab.csv",'w') as filename2:

        for i in range(0, numRuns):
            # Calculate the time taken
            # start time
            print("Started Scraping run:",i)
            start_run = time.time()
            # .Cursor() returns an object that you can iterate or loop over to access the data collected.
            # Each item in the iterator has various attributes in semi- structured Format.
            # Full tweet text including retweeted text were stored as big text file for text processing.
            ukrainetweets = tweepy.Cursor(api.search_tweets, q=search_words, lang="en", since_id=date_since, tweet_mode='extended').items(numTweets)
            # Store these tweets into a python list
            tweet_list = [tweet for tweet in ukrainetweets]
            csv_header= ['Tweet_Text']
            # Set Counter Zero to Calculate the Total Number of Scraped Tweets :
            noTweets = 0
            for tweet in tweet_list:
                try:
                    text = tweet.retweeted_status.full_text
                except AttributeError:  # Not a Retweet
                    text = tweet.full_text
                Extracted_Text=[text]

                # Text information stored in separate big csv file,later for text analysis.
                write = csv.writer(filename2, dialect='excel')
                write.writerows([Extracted_Text])
                filename2.flush()

                # Store all the extracted tweets into a semi-structured JSON file ,which will be useful for inserting the data into MONGODB(part 2)
                filename.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                # increase counter - noTweets
                noTweets += 1

           # print(df.head(10))
            # Run ended:
            end_run = time.time()
            duration_run = round(end_run - start_run, 2)

            print('Total Number of tweets scraped for run {} is {}'.format(i, noTweets))
            print('Time taken for  {} run to complete is {}'.format(i, duration_run))
            print("Sleeping Time 15 Minutes started")
            time.sleep(900)  # 15 minute sleep time
            print("Sleeping Time 15 Minutes Ended:) Scrap again!")

    print('Twitter Scraping has completed!')

if __name__ == "__main__":
    ## Arguments:
    # Search_Topic -> define a string of keywords for this function to extract
    # Date_since -> define a date from which to start extracting the tweets
    # NumberofTweets -> number of tweets to Scraped per run
    # NumberOfRun -> Calling API every 15 minutes to prevent Twitter Api limits( 900 requests / 15 Min # PER USER - Elevated Access)

    Search_Topic = "#ukraineWar OR #UkraineWar OR #ukraine OR #UKRAINE OR #UkraineRussiaWar OR #RussiaUkrainelatestnews OR #PutinIsaWarCriminal"
    Date_since = "2022-02-02"
    NumberofTweets = 2000
    NumberofRuns = 3
    # Call the Scraping function
    scraptwitter_tweets_sab(Search_Topic, Date_since, NumberofTweets, NumberofRuns)


'''
Reference:
1)https://python.plainenglish.io/scraping-tweets-with-tweepy-python-59413046e788
2)https://github.com/leowgriffin/tweets_analysis_hkprotests_2019/blob/master/scraping_tweets.py

'''