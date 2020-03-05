from fastapi import FastAPI
from crawler import TwitterCrawler
from pydantic import BaseModel

class Item(BaseModel):
  hashtag: str

app = FastAPI()

@app.get('/')
def root():

  return {"message": "Hello World!"}

@app.post('/hashtag/')
async def sendHashtag(hashtag: Item):

  clr = TwitterCrawler()
  print(hashtag.hashtag)
  clr.persist_tweets(hashtag.hashtag)

  return "Hashatg enviada: "+hashtag.hashtag





