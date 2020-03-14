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

    def pre_process(self, text):

        text = text.lower()

        text = re.sub('(\\n)+', ' ', text)

        text = ' '.join([word for word in text.split() if word not in stopwords.words(
            'portuguese') and word not in string.punctuation])

        text = norm('NFKD', text).encode('ascii', 'ignore').decode()

        text = re.sub('\@\S*', '', text)

    #     text = ''.join([char for char in text if char not in string.punctuation])

        return text

    def predict(self, samples):

        samples = [self.pre_process(sample) for sample in samples]
        preds = self.classifier.predict(samples)
        preds_proba = self.classifier.predict_proba(samples)

        preds_proba = [pred_proba.max() for pred_proba in preds_proba]

        return {"preds": preds[0],
                "probabilities": preds_proba[0]}
