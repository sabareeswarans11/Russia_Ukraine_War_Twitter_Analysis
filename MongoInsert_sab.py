"""
coding:utf-8
Storing and Retrieving to Process from a Semi-Structured Database Server MongoDB
Author: Sabareeswaran Shanmugam
"""
import copy
import json
import os
import pymongo.errors
from pymongo import MongoClient
from pymongo.errors import OperationFailure
""" Using geocoder some of the missing coordinates in twitter attribute is replaced by taking the attribute location"""
import geocoder
from geopy.exc import GeocoderTimedOut

# setting Absolute Path
sab_absolute_path = os.path.dirname(os.path.abspath(__file__))

def MongoInsert():
    try:
        client = MongoClient(host="localhost", port=27017)
        db = client['twitter_scraped_data_sab']
        db_collection = db['UkraineTweets_sab']
        try:
            client.server_info()
            print("Connected to MongoDB Successfully")
        except OperationFailure as e:
            print(e)
    except Exception as e:
        print(e)
    with open(sab_absolute_path+ '/twitter_data/UkraineRussiaWar6000_Tweets.json', 'r') as f:
        print("Inserting tweets in MongoDB")
        NoOfTweetsInserted = 0
        for line in f:
            if (line == '\n'):
                continue
            tweet = json.loads(line)  # load it as Python dict/document for db

            tweet_copy = copy.copy(tweet)

            # place_data always return null --Twitter API , so here location of the tweet is replaced in place_type.
            for x in tweet_copy.keys():
                if tweet['place'] is None:
                    try:
                        if tweet['user']['location'] is not None:
                            result = geocoder.arcgis(tweet['user']['location'])
                            tweet['place'] = tweet['user']['location']
                            tweet['coordinates'] = (result.x, result.y)
                    except GeocoderTimedOut as e:
                        pass
                try:
                    db_collection.insert_one(tweet)
                    NoOfTweetsInserted+=1
                except pymongo.errors.DuplicateKeyError:
                    continue
            print("Total mongo insert done :", NoOfTweetsInserted)
        print("Completed tweets insert in MongoDB")
        client.close  # close db connection
    f.close()  # close file handle

if __name__ == "__main__":
    MongoInsert()

'''
Reference:
1)https://www.geeksforgeeks.org/mongodb-python-insert-update-data/
2)https://stackoverflow.com/questions/36544396/twitter-api-returns-null-for-coordinates-and-retweets
'''
