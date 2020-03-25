import tweepy
from config import *
import pandas as pd
import numpy as np
import pymongo
import time
import requests


class TwitterCrawler:

    def __init__(self):
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.access_token = ACESS_TOKEN
        self.access_token_secret = ACESS_TOKEN_SECRET
        self.mongo_client = pymongo.MongoClient(
            'mongodb+srv://brunobelluzzo:bruno0911@twitteranalysis-zrfix.mongodb.net/test?retryWrites=true&w=majority')

    def persist_tweets(self, hashtag, limit_date=None):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        db = self.mongo_client.Twitter

        dates = []
        tweets = []
        actual_date = 0
        count_tweets = 0
        final_obj = {"hashtag": hashtag,
                     "tweets": []}

        db.tweets.insert_one(final_obj)

        for tweet in tweepy.Cursor(api.search, q=hashtag,
                                   lang="pt",
                                   tweet_mode="extended").items():
            try:
                obj = {"date": "",
                       "tweet_text": ""}

                ts = tweet.created_at

                date = str(ts.day)+"/"+str(ts.month)+"/"+str(ts.year)

                # if actual_date == 0:

                #     actual_date = date

                # if date != actual_date:

                #     actual_date = date

                # if limit_date:
                #     if date == limit_date:
                #         break

                pred = requests.post(
                    'http://localhost:8000/predict', json={'tweet': tweet._json["full_text"]})

                resp = pred.json()
                obj["date"] = date
                obj["tweet_text"] = tweet._json["full_text"]
                obj['sentiment'] = resp

                db.tweets.update_one({'hashtag': hashtag}, {
                    '$push': {'tweets': obj}})
            except Exception as e:
                print(str(e))
                time.sleep(180)
                continue

        return "Hashtag "+hashtag+" inserida no banco com sucesso."

    def get_tweets_day(self, hashtag):

        print('get')
