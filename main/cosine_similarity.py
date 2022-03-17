import numpy as np
import pandas as pd
from extract_keywords import *
import tweepy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import tweepy
import re
from textblob import TextBlob
import csv
from collections import Counter
from tweet_api import *
from extract_keywords import *
import itertools
from pandas import DataFrame
from difflib import SequenceMatcher

api = get_api()

def two_word_grouping(s, n):
    if n == 1:
        return list(itertools.combinations(s, 1))
    else:
        return list(itertools.combinations(s, 2))


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

WORD = re.compile(r"\w+")

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)



def cosine_similarity_model(input_tweet):

    new_string_list = []
    query_string = ""
    searched_tweets = []
    final_hashtag_list = []
    suffix = ' OR '
    max_tweets = 500

    get_keyWords = generateKeyword(input_tweet)

    word_groupings = two_word_grouping(get_keyWords, len(get_keyWords))

    for i in range(len(word_groupings)):
      new_string_list.append(' '.join(word_groupings[i]))

    for i in range(len(new_string_list)):
        query_string += '('+new_string_list[i]+')' + ' OR '
        if i==20:
          break
    query_string = re.sub(re.escape(suffix) + '$', '', query_string)
    query = "{} -filter:retweets -filter:mentions".format(query_string)

    for tweet in tweepy.Cursor(api.search,tweet_mode='extended',q=query,count=1000,lang="en",since="2017-04-03").items(500):
        searched_tweets.append(tweet.full_text)
    df = pd.DataFrame(searched_tweets,columns=['tweets'])
    df['hashtags']=df['tweets'].str.lower().str.findall(r'#.*?(?=\s|$)')
    hashtagged_df = df[df['hashtags'].map(lambda d: len(d)) > 0]
    hashtagged_df = hashtagged_df.reset_index(drop=True)
    hashtagged_df_new = hashtagged_df.copy()
    hashtagged_df_new['tweets'] = hashtagged_df_new['tweets'].str.lower()

    def similar(a,b):
        return SequenceMatcher(None, a, b).ratio()

    #test
    hashtagged_df_new['Cosine_sim'] =  similar(' initialization','Initialization')

    for i in range(37):
      hashtagged_df_new['Cosine_sim'][i] = similar(input_tweet,hashtagged_df_new['tweets'][i])

    hashtagged_df_new_order = hashtagged_df_new.sort_values(['Cosine_sim'], ascending=[False])

    hashtag_list = list(set(list(np.concatenate(hashtagged_df_new_order.head(10)['hashtags'].tolist()))))[:11]
    #print(hashtag_list)
    if '#' in hashtag_list:
        hashtag_list.remove('#')
    #print(hashtag_list)
    return hashtag_list
