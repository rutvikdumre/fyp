from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import tweepy
import re
import pandas as pd
from textblob import TextBlob
import csv
from collections import Counter
from .tweet_api import * 
from .extract_keywords import *
from .model import *
import itertools



api = get_api()


#print('Write a tweet:')

def gethash(tweet_input):
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    nltk.download('stopwords')

    appropriate_hashtag_list = tweet_similarity_model(tweet_input)

    if tweet_input != "":
        return appropriate_hashtag_list

