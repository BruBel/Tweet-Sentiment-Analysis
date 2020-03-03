import tweepy
from config import *
import pandas as pd
import numpy as np

class TwitterCrawler:

  def __init__(self):
    self.consumer_key = CONSUMER_KEY
    self.consumer_secret = CONSUMER_SECRET
    self.access_token = ACESS_TOKEN
    self.access_token_secret = ACESS_TOKEN_SECRET

  def get_tweets(self, hashtag, limit_date=None):

    auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
    auth.set_access_token(self.access_token, self.access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    df = pd.DataFrame()

    dates = []
    tweets = []
    actual_date = 0
    count_tweets = 0
    for tweet in tweepy.Cursor(api.search,q=hashtag,
                           lang="pt",
                           tweet_mode="extended").items():

      ts = tweet.created_at

      date = str(ts.day)+"/"+str(ts.month)+"/"+str(ts.year)

      if actual_date == 0:

        actual_date = date

      if date != actual_date:
        
        actual_date = date

      if limit_date:
        if date == limit_date:
          break

      dates.append(date)
      tweets.append(tweet._json["full_text"])
    
    df['date'] = dates
    df['tweet'] = tweets

    return df

  def get_tweets_day(self, hashtag):

    print('get')
