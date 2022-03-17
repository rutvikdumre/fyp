import itertools
import tweepy
import re
from .tweet_api import *
from .extract_keywords import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from collections import Counter

api = get_api()

def two_word_grouping(s, n):
    if n == 1:
        return list(itertools.combinations(s, 1))
    else:
        return list(itertools.combinations(s, 2))


def tweet_similarity_model(input_tweet):

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

    for tweet in tweepy.Cursor(api.search_tweets,tweet_mode='extended',q=query,count=1000,lang="en").items(900):
        searched_tweets.append(tweet.full_text)

    searched_tweets_string = "".join(searched_tweets)

    hashtag_list = re.findall(r"#(\w+)", searched_tweets_string)

    for i in hashtag_list:
      final_hashtag_list.append(i[0].upper() + i[1:])

    word_count = Counter(final_hashtag_list)
    word_frequency_count = [key for key, _ in word_count.most_common(10)]

    hashtag_count = []
    for i in word_frequency_count:
        hashtag_count.append('#'+i)

    return hashtag_count
