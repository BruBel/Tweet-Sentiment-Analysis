from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crawler import TwitterCrawler
from pydantic import BaseModel
import pymongo
from config import *
from classifier import SentimentClassifier


class Item(BaseModel):
    hashtag: str


app = FastAPI()


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
