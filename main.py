from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crawler import TwitterCrawler
from pydantic import BaseModel
import pymongo
from config import *
from classifier import SentimentClassifier
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware


class Item(BaseModel):
    hashtag: str


app = FastAPI()

origins = [

    "http://localhost",
    "http://localhost:5057",
    "http://localhost:5057/getHashtag",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():

    return {"message": "Hello World!"}


@app.post('/hashtag')
def sendHashtag(hashtag: Item):

    clr = TwitterCrawler()
    print(hashtag.hashtag)
    clr.persist_tweets(hashtag.hashtag)

    return "Hashatg enviada: "+hashtag.hashtag


@app.post('/predict')
def predict_sentiment(tweet: dict):

    sentiment_clf = SentimentClassifier('sentiment-classifier-v0.pkl')
    sentiment = sentiment_clf.predict([str(tweet['tweet'])])

    return {'sentiment': sentiment}


@app.get('/getAllHashtags')
def get_all_hashtags():
    mongo_client = pymongo.MongoClient(
        'mongodb+srv://brunobelluzzo:bruno0911@twitteranalysis-zrfix.mongodb.net/test?retryWrites=true&w=majority')

    db = mongo_client.Twitter


@app.get('/getHashtag/{hashtag}')
def get_hashtag(hashtag: str):

    mongo_client = pymongo.MongoClient(
        'mongodb+srv://brunobelluzzo:bruno0911@twitteranalysis-zrfix.mongodb.net/test?retryWrites=true&w=majority')

    db = mongo_client.Twitter

    value = db.tweets.find_one({'hashtag': hashtag})
    value.pop('_id')

    dates_positive = [date['date'] for date in value['tweets']
                      if date['sentiment']['sentiment']['preds'] == 'Positivo']

    dates_negative = [date['date'] for date in value['tweets']
                      if date['sentiment']['sentiment']['preds'] == 'Negativo']

    new_dict_positive = {}
    for date in sorted(dict(Counter(dates_positive))):

        new_dict_positive[date] = dict(Counter(dates_positive))[date]

    new_dict_negative = {}
    for date in sorted(dict(Counter(dates_negative))):

        new_dict_negative[date] = dict(Counter(dates_negative))[date]

    return {'positive response': new_dict_positive, 'negative response': new_dict_negative}
