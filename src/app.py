from fastapi import FastAPI
from crawler import TwitterCrawler

app = FastAPI()

@app.post('/hashtag')
def sendHashtag(hashtag: str):

  clr = TwitterCrawler()

  df = clr.persist_tweets(hashtag)

  return "Hashatg enviada: "+hashtag



