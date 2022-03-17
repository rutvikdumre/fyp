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

api = get_api()

def two_word_grouping(s, n):
    if n == 1:
        return list(itertools.combinations(s, 1))
    else:
        return list(itertools.combinations(s, 2))

def extract_hashtags(text):
    hashtag_list = []
    for word in text.split():
        if word[0] == '#':
            hashtag_list.append(f'#{word[1:].lower()}')
    return hashtag_list



def naive_bayes_model(input_tweet):

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
    print(new_string_list)
    for i in range(len(new_string_list)):
        query_string += '('+new_string_list[i]+')' + ' OR '
        if i==20:
          break
    query_string = re.sub(re.escape(suffix) + '$', '', query_string)
    print(query_string)
    query = "{} -filter:retweets -filter:mentions".format(query_string)

    for tweet in tweepy.Cursor(api.search,tweet_mode='extended',q=query,count=1000,lang="en",since="2017-04-03").items(500):
        searched_tweets.append(tweet.full_text)
    df = pd.DataFrame(searched_tweets,columns=['tweets'])
    df['tweets'] =df['tweets'].str.replace(".", "")
    print(df)
    df['hashtags']=df['tweets'].apply(lambda x: extract_hashtags(x) )
    hashtagged_df = df[df['hashtags'].map(lambda d: len(d)) > 0]
    hashtagged_df = hashtagged_df.reset_index(drop=True)
    hashtagged_df_new = hashtagged_df.copy()
    hashtagged_df_new['tweets'] = hashtagged_df_new['tweets'].str.lower()
    print(hashtagged_df_new)
    df.to_csv('out.csv', index=False)

    a=np.concatenate(hashtagged_df.hashtags).tolist()
    word_count = Counter(a)
    if len(list(set(word_count))) >= 200:
      word_frequency_count = [key for key, _ in word_count.most_common(200)]
    else:
      word_frequency_count = [key for key, _ in word_count.most_common(len(list(set(word_count))))]

    my_dict = {}
    list_of_words = list(get_keyWords)
    n = hashtagged_df_new['tweets'].count()
    for i in word_frequency_count:
      prob = 1
      for j in list_of_words:
        count = (hashtagged_df_new[(hashtagged_df_new['tweets'].str.contains(j)) & (hashtagged_df_new['tweets'].str.contains(i))])['tweets'].count()
        if count != 0:
          prob *= count/n
        if count == 0:
          prob *= 1/n
      new = prob
      #print(i, prob)
      my_dict[i] = new

    final_list = sorted(my_dict, key=my_dict.get, reverse=True)[:10]

    if '#' in final_list:
        final_list.remove('#')

    return final_list
