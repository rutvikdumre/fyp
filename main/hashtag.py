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
"""trends_US = api.trends_place(23424977)
trends_world = api.trends_place(1)
topic_US = []
topic_World = []

for i in trends_US:
    for trend in i['trends']:
        topic_US.append(trend['name'])
for i in topic_US:
    if i.startswith('#'):
        st.sidebar.write(i)

st.sidebar.header("Trending Twitter hashtags (World)")
for i in trends_world:
    for trend in i['trends']:
        topic_World.append(trend['name'])
for i in topic_World:
    if i.startswith('#'):
        st.sidebar.write(i)"""

#print('Write a tweet:')

def gethash(tweet_input):
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    appropriate_hashtag_list = tweet_similarity_model(tweet_input)

    if tweet_input != "":
        return appropriate_hashtag_list

