# -*- coding: utf-8 -*-
"""
Created on Sat May 26 10:06:24 2018

@author: Yus
"""

import tweepy
import csv
import pandas as pd
import os

def download_tweets(file_name, query, n_tweets, since_date):
    
    # Add the credentials of your Twitter application
    consumer_key = ''
    consumer_secret = ''
    access_token = '-'
    access_token_secret = ''
    
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True, 
                     wait_on_rate_limit_notify=True)
    
    if api: 
        print("Connected to Twitter's API...")
    else:
        print("Can't authenticate.")
    
    cnt = 0
    print("Downloading tweets on",file_name,"...")
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        while cnt < n_tweets: 
            try:
                new_tweets = api.search(q=query, count = 100)
                
                for tweet in new_tweets:
                    writer.writerow([tweet.text.encode('utf-8')])
                    cnt += len(new_tweets)
                    print("Current tweets downloaded",cnt)
                    
            except tweepy.TweepError as e:
                print("Error:",str(e))
                break


# Open/Create a file to append data
os.chdir("C://Users//Yus//Desktop")

# Set params of the query
query = "#AvengersInfinityWar"
tweets = 5000
file = "avengers_nuevo_tweets.csv"
since_date = "2018-04-01"

# Download tweets
download_tweets(file, query, tweets, since_date)




# -----------------------------------------------------------------------------
