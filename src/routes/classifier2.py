import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

from nltk.corpus import stopwords
import string
import re
from bs4 import BeautifulSoup
import string
from unicodedata import normalize as norm


class SentimentClassifier:

  def __init__(self, path_to_model):
    self.classifier = joblib.load(path_to_model)


  def predict(self, samples):
    
    preds = self.classifier.predict(samples)
    preds_proba = self.classifier.predict_proba(samples)

    preds_proba = [pred_proba.max() for pred_proba in preds_proba]
    
    return {"preds": preds,
            "probabilities": preds_proba}