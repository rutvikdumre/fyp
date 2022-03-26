# Import the Twython class
from numpy import positive
from twython import Twython
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import tweepy
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import re
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import re
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os
import nltk
import heapq
from datetime import datetime




consumer_key = "Tm30Tmmk1eaEzbi23Nm3NU1g5"
consumer_secret = "jId4w7i1QLJGqv3JnlM33N9ZzZEhP1QmYu6RzaBYarrNM5HAzG"
access_token = "1390534356796514304-5KUsYqQaXJXxKwauEupXT7UtkYLAmY"
access_token_secret = "U4nDzR99UsH8aCuKB9ntLGbZLCwwoDkLLjt0A3FvwngT1"
# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)




# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)


    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return ["Positive",sentiment_dict['compound']]

    elif sentiment_dict['compound'] <= - 0.05 :
        return ["Negative",sentiment_dict['compound']]

    else :
        return ["Neutral",sentiment_dict['compound']]

def twitter_credentials():
    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = 'Tm30Tmmk1eaEzbi23Nm3NU1g5'
    credentials['CONSUMER_SECRET'] = 'jId4w7i1QLJGqv3JnlM33N9ZzZEhP1QmYu6RzaBYarrNM5HAzG'
    credentials['ACCESS_TOKEN'] = '1390534356796514304-5KUsYqQaXJXxKwauEupXT7UtkYLAmY'
    credentials['ACCESS_SECRET'] = 'U4nDzR99UsH8aCuKB9ntLGbZLCwwoDkLLjt0A3FvwngT1'

    # Save the credentials object to file
    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)
    
def twitter_query(query):
    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    query+= "-filter:retweets"

    # Create our query
    query = {'q': query,
            'result_type': 'mixed',
            'count': 100,
            'lang': 'en',
            'geocode':'',
            'tweet_mode': 'extended' 
            }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'hashtags':[], 'location':[]}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['full_text'])
        dict_['favorite_count'].append(status['favorite_count'])
        dict_['hashtags'].append([hashtag['text'] for hashtag in status['entities']['hashtags']])
        dict_['location'].append(status['user']['location'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    sentiment=[]
    for i in df['text']:
        sentiment+=[sentiment_scores(i)[0]]
    df['sentiment']=sentiment
    try:
        pos=df['sentiment'].value_counts()['Positive']
    except:
        pos=0
    try:
        neg=df['sentiment'].value_counts()['Negative']
    except:
        neg=0
    try:
        neu=df['sentiment'].value_counts()['Neutral']
    except:
        neu=0
    print(df.shape)
    return df,pos,neg,neu


def twitter_profile_query(query):
    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    query+= "-filter:retweets"

    # Create our query
    query = {'q': query,
            'result_type': 'mixed',
            'count': 100,
            'lang': 'en',
            'geocode':'',
            'tweet_mode': 'extended' 
            }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'hashtags':[], 'location':[]}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['full_text'])
        dict_['favorite_count'].append(status['favorite_count'])
        dict_['hashtags'].append([hashtag['text'] for hashtag in status['entities']['hashtags']])
        dict_['location'].append(status['user']['location'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    sentiment=[]
    for i in df['text']:
        sentiment+=[sentiment_scores(i)[1]]
    df['sentiment']=sentiment
    try:
        pos=df['sentiment'].value_counts()['Positive']
    except:
        pos=0
    try:
        neg=df['sentiment'].value_counts()['Negative']
    except:
        neg=0
    try:
        neu=df['sentiment'].value_counts()['Neutral']
    except:
        neu=0
    print(df.shape)
    return df


def getinfo(name):
    

    # assign the values accordingly

    consumer_key = 'as6IxOQ0arO7AznKoPUfLQt5l'
    consumer_secret = 'a9CHQVAvui2BuxXVKAqBHOBDOiGex1iFAb8vaHtKDT91ni4nBz'
    access_token =  '1390534356796514304-AX2lcuHToECxxzl5HtBqU4SPZD05lc'
    access_token_secret = 'MbXWOuYOjljxe90NgOJGiYSu46fX7AQ020RtwpaKOwQyG'
    
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
    # set access to user's access key and access secret 
    auth.set_access_token(access_token, access_token_secret)
    
    # calling the api 
    api = tweepy.API(auth)

    # the screen name of the user
    screen_name = name
    
    # fetching the user
    user = api.get_user(screen_name)
    return user._json
    
    
def sentplot(df):
    """fig, ax = plt.subplots()
    color_dict = {'Positive':'#6ab04c', 'Negative':'#eb4d4b', 'Neutral':'#22a6b3'}
    fig=df['sentiment'].value_counts().plot(ax=ax, kind='barh')"""
    fig = px.pie(df, values=df['sentiment'].value_counts().values, names=df['sentiment'].value_counts().index)
    fig.write_html('./main/templates/main/sent.html')
    
    #return plt

def tweetClean(df):
    Tweet_Texts=df['text'].values
    Tweets_String=str(Tweet_Texts)
    Tweet_Texts_Cleaned = Tweets_String.lower()
    Tweet_Texts_Cleaned=re.sub(r'@\w+', ' ', Tweet_Texts_Cleaned)
    Tweet_Texts_Cleaned=re.sub(r'http\S+', ' ', Tweet_Texts_Cleaned)
    # Deleting everything which is not characters
    Tweet_Texts_Cleaned = re.sub(r'[^a-z A-Z]', ' ',Tweet_Texts_Cleaned)
    
    # Deleting any word which is less than 3-characters mostly those are stopwords
    Tweet_Texts_Cleaned= re.sub(r'\b\w{1,2}\b', '', Tweet_Texts_Cleaned)
    
    # Stripping extra spaces in the text
    Tweet_Texts_Cleaned= re.sub(r' +', ' ', Tweet_Texts_Cleaned)
    
    return Tweet_Texts_Cleaned

def wordcloud(Tweet_Texts_Cleaned):
    # Creating the custom stopwords
    customStopwords=list(STOPWORDS)+ ['cases','corona','virus','people','will']
    
    wordcloudimage = WordCloud(
                            max_words=100,
                            max_font_size=500,
                            font_step=2,
                            stopwords=customStopwords,
                            background_color='white',
                            width=1000,
                            height=720
                            ).generate(Tweet_Texts_Cleaned)
    
    plt.figure(figsize=(15,7))
    plt.axis("off")
    plt.imshow(wordcloudimage)
    #wordcloudimage
    #plt.show()
    return plt

twitter_credentials()

def inf_calc_users(pop,reach):

  x_pop = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'x_pop')      #final['popularity_score'].to_numpy()
  x_reach = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'x_reach')    #final['reach_score'].to_numpy()

  x_inf  = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'x_inf')

  x_pop['low'] = fuzz.trimf(x_pop.universe, [0, 0, 0.5])
  x_pop['med'] = fuzz.trimf(x_pop.universe, [0, 0.5, 1])
  x_pop['high'] = fuzz.trimf(x_pop.universe, [0.5, 1, 1])

  x_reach['low'] = fuzz.trimf(x_reach.universe, [0, 0, 0.5])
  x_reach['med'] = fuzz.trimf(x_reach.universe, [0, 0.5, 1])
  x_reach['high'] = fuzz.trimf(x_reach.universe, [0.5, 1, 1])

  x_inf['low'] = fuzz.trimf(x_inf.universe, [0, 0, 0.5])
  x_inf['med'] = fuzz.trimf(x_inf.universe, [0, 0.5, 1])
  x_inf['high'] = fuzz.trimf(x_inf.universe, [0.5, 1, 1])


  rule1 = ctrl.Rule(x_pop['low'] & x_reach['low'], x_inf['low'])
  rule2 = ctrl.Rule((x_pop['med'] | x_reach['med']), x_inf['med'])
  rule3 = ctrl.Rule(x_pop['high'] | x_reach['high'], x_inf['high'])

  influence_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  influence = ctrl.ControlSystemSimulation(influence_ctrl)


  # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
  # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
  influence.input['x_pop'] = pop
  influence.input['x_reach'] = reach

  # Crunch the numbers
  influence.compute()
  inf=influence.output['x_inf']

  return inf

def score_compare(users):
    screenname = []
    no_ofLikes = []
    no_ofFollowing = []
    no_ofTweetsCount = []
    no_ofFollowers = []
    
    api = tweepy.API(auth)
    error=[]
    for name in users:
        try:
            results = api.get_user(screen_name=name)
            screenname.append(results.screen_name)
            no_ofFollowers.append(results.followers_count)
            no_ofLikes.append(results.favourites_count)
            no_ofFollowing.append(results.friends_count)
            no_ofTweetsCount.append(results.statuses_count) 
        except:
            error+=['Problem with the username:{}'.format('name')]
            print(error)

        dict_tweets = {'screenname': screenname, 'no_of_likes':no_ofLikes, 'no_of_followers':no_ofFollowers, 'no_of_following':no_ofFollowing, 'tweet_count':no_ofTweetsCount}
        df_tweets = pd.DataFrame(dict_tweets)
        df_tweets['reach_score']=df_tweets['no_of_followers']-df_tweets['no_of_following']
        df_tweets['popularity_score']=df_tweets['no_of_likes']+df_tweets['tweet_count']
        
        tweet=df_tweets[df_tweets.tweet_count == df_tweets.tweet_count.max()]
        fol= df_tweets[df_tweets.no_of_followers == df_tweets.no_of_followers.max()]
        like = df_tweets[df_tweets.no_of_likes == df_tweets.no_of_likes.max()]

    pd.options.plotting.backend = "plotly"


    # Likes
    


    fig0 = px.pie(df_tweets, values = "no_of_likes", names='screenname', title = "Distribution of Likes", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white', hole=.3)
    fig0.write_html('./main/templates/main/likes.html')

    fig1 = px.pie(df_tweets, values = "no_of_followers", names='screenname', title = "Distribution of Followers", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white',  hole=.3)
    fig1.write_html('./main/templates/main/followers.html')

    # Popularity Score and Reach score
    fig2= px.bar(df_tweets, y = "screenname", x = "popularity_score",
       labels = {"screenname": "Twitter Screen name", "popularity_score": "Popularity Score"},
       orientation = 'h',color = "popularity_score", color_continuous_scale = px.colors.diverging.Spectral, template='plotly_white')
    fig2.write_html("./main/templates/main/pop.html")

    fig3 = px.bar(df_tweets, y = "screenname", x = "reach_score",
       labels = {"screenname": "Twitter Screen name", "reach_score": "Reach Score"},
       orientation = 'h',color = "reach_score", color_continuous_scale =px.colors.diverging.Spectral, template='plotly_white')
    fig3.write_html("./main/templates/main/reach.html")

    # Normalisation and Influencer score calculation

    scaler = MinMaxScaler(feature_range=(0,1))
    df_tweets[['popularity_score', 'reach_score']]= scaler.fit_transform(df_tweets[['popularity_score', 'reach_score']])

    inf=[]
    for index, i in df_tweets.iterrows():
      inf+=[inf_calc_users(i['popularity_score'],i['reach_score'])]
    df_tweets['inf']=inf

    infc= df_tweets[df_tweets.inf == df_tweets.inf.max()]

    fig4 = px.bar(df_tweets, y = "screenname", x = "inf",
       labels = {"screenname": "Twitter Screen name", "inf": "Influence Score"},
       orientation = 'h',color = "inf", color_continuous_scale = px.colors.diverging.Spectral, template='plotly_white')
    fig4.write_html("./main/templates/main/inf.html")
    
    return tweet,fol,like,infc



def proposed_getdata(query):
    try:
        os.remove("topic.json")
    except:
        pass
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    # Create our query
    query = {'q': query,
            'result_type': 'mixed',
            'count': 100,
            'lang': 'en',
            #'geocode':'21.145800,79.088158,100000km' 
            }
    
    data_json = []

    for status in python_tweets.search(**query)['statuses']:
        dict_ = {"text": "", "created_at": "", "entities":{}, "user": {}, "retweet_count": "None",  "id":""}
        #dict_ = dict.fromkeys(['user', 'created_at', 'text', 'retweet_count', 'entities', 'location'])
        dict_user = {
            "lang" :status['user']['lang'],
            "created_at" :status['user']['created_at'],
            "statuses_count" :status['user']['statuses_count'],
            "description" :status['user']['description'],
            "friends_count" :status['user']['friends_count'],
            "url": status['user']['url'],
            "profile_image_url_https": status['user']['profile_image_url_https'],
            "followers_count": status['user']['followers_count'],
            "screen_name" :status['user']['screen_name'],
            "location": status['user']['location'],
            "favourites_count": status['user']['favourites_count'],
            "verified": str(status['user']['verified']),
            "id":status['user']['id'], 
            "name": status['user']['name'] 
            }
        dict_entities = {
        "user_mentions": status['entities']['user_mentions'],
        "hashtags": status['entities']['hashtags'],
        "urls": status['entities']['urls']
        }
        dict_['user'].update(dict_user)
        dict_['entities'].update(dict_entities)
        dict_['created_at'] = status['created_at']
        dict_['text'] = status['text']
        dict_['retweet_count'] = status['retweet_count']
        dict_['id'] = status['id']
        
        #print(dict_)
        
    
        with open("topic.json", "a") as outfile:
            json_obj = json.dumps(dict_)
            outfile.write(json_obj)
            outfile.write("\n")
            
    tweets_file = open('topic.json')
    
    
def fuzzy():
    tweets_file = open('topic.json')
    tweet_obj = []
    for line in tweets_file:
        tweet_obj.append(json.loads(line))
    try:
        os.remove('GFG.csv')
    except:
        pass
    os.system('python pagerank.py -f, --file=topic.json')
    pagerank= pd.read_csv('GFG.csv')
    pagerank.rename(columns = {'name':'screenname'}, inplace = True)
    user_twitter_handle=[]
    for i in tweet_obj:
        user_twitter_handle.append('@'+str(i['user']['screen_name']))
    for i in pagerank['screenname']:
        user_twitter_handle.append('@'+str(i))
    user_twitter_handle=list(set(user_twitter_handle))
        
    '''list_tweets = []
    
    for x in range(0, len(user_twitter_handle)):
        # The Twitter user who we want to get tweets from
        name = user_twitter_handle[x]
        try:
        # Calling the user_timeline function with our parameters
            results = api.user_timeline(user_id=name, count=10)
        # foreach through all tweets pulled
            for tweet in results:
        # printing the text stored inside the tweet object
                list_tweets.append(tweet.text)
        except:
            continue

    df_tweets = DataFrame(list_tweets, columns=['Tweets'])
    df_tweets.to_csv(r'tweets.csv', index=False)'''
    
    screenname = []
    no_ofLikes = []
    no_ofFollowing = []
    no_ofTweetsCount = []
    no_ofFollowers = []

    #print("total users: ", len(user_twitter_handle))
    
    for x in range(0, len(user_twitter_handle)):
        name = user_twitter_handle[x]
        #print(name)
        try:
            #print('Calling the user_timeline function with our parameters')
            results = api.get_user(screen_name=name)
            #print(results)
            screenname.append(results.screen_name)
            no_ofFollowers.append(results.followers_count)
            no_ofLikes.append(results.favourites_count)
            no_ofFollowing.append(results.friends_count)
            no_ofTweetsCount.append(results.statuses_count)
        except:
            continue
        
    dict_tweets = {'screenname': screenname, 'no_of_likes':no_ofLikes, 'no_of_followers':no_ofFollowers, 'no_of_following':no_ofFollowing, 'tweet_count':no_ofTweetsCount}
    """print('--------------------------------------------------------')
    print()
    print(dict_tweets)
    print()
    print('--------------------------------------------------------')"""
    df_tweets = pd.DataFrame(dict_tweets)
    
    df_tweets['reach_score']=df_tweets['no_of_followers']-df_tweets['no_of_following']
    df_tweets['popularity_score']=df_tweets['no_of_likes']+df_tweets['tweet_count']
    
    final = pd.merge(pagerank, df_tweets, how='outer', on=['screenname'])
    final = final.dropna()
    scaler = MinMaxScaler(feature_range=(0,1))
    final[["reach_score", "popularity_score", "pagerank"]] = scaler.fit_transform(final[["reach_score", "popularity_score", "score"]])

    final = final.drop("score", axis=1)
    
    #final.to_csv('combined.csv')
    fna=final.dropna()
    
    inf=[]
    for index, i in fna.iterrows():
        inf+=[inf_calc(i['popularity_score'],i['reach_score'],i['pagerank'])]
    fna['inf']=inf
    
    try:
        os.remove('combined_inf.csv')
    except:
        pass
    fna.to_csv('combined_inf.csv')
    
    
def inf_calc(pop,reach,page):
    x_pop = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'x_pop')      #final['popularity_score'].to_numpy()
    x_reach = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'x_reach')    #final['reach_score'].to_numpy()
    x_page= ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'x_page')      #final['score'].to_numpy()

    x_inf  = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'x_inf')
    
    x_pop['low'] = fuzz.trimf(x_pop.universe, [0, 0, 0.5])
    x_pop['med'] = fuzz.trimf(x_pop.universe, [0, 0.5, 1])
    x_pop['high'] = fuzz.trimf(x_pop.universe, [0.5, 1, 1])

    x_reach['low'] = fuzz.trimf(x_reach.universe, [0, 0, 0.5])
    x_reach['med'] = fuzz.trimf(x_reach.universe, [0, 0.5, 1])
    x_reach['high'] = fuzz.trimf(x_reach.universe, [0.5, 1, 1])

    x_page['low'] = fuzz.trimf(x_page.universe, [0, 0, 0.5])
    x_page['med'] = fuzz.trimf(x_page.universe, [0, 0.5, 1])
    x_page['high'] = fuzz.trimf(x_page.universe, [0.5, 1, 1])
    
    x_inf['low'] = fuzz.trimf(x_inf.universe, [0, 0, 0.5])
    x_inf['med'] = fuzz.trimf(x_inf.universe, [0, 0.5, 1])
    x_inf['high'] = fuzz.trimf(x_inf.universe, [0.5, 1, 1])
    rule1 = ctrl.Rule(x_pop['low'] & x_reach['low'], x_inf['low'])
    rule2 = ctrl.Rule((x_pop['med'] | x_reach['med'] | x_page['med']), x_inf['med'])
    rule3 = ctrl.Rule(x_pop['high'] | x_reach['high'] | x_page['high'], x_inf['high'])

    influence_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    influence = ctrl.ControlSystemSimulation(influence_ctrl)


    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    influence.input['x_pop'] = pop
    influence.input['x_reach'] = reach
    influence.input['x_page']= page

    # Crunch the numbers
    influence.compute()
    inf=influence.output['x_inf']

    return inf

def combine():
    df= pd.read_csv('combined_inf.csv')
    df = df[['screenname','inf']]
    tweets= pd.read_json('topic.json', lines=True) #remove empty line at the end of JSON if error occurs


    temp={'screenname':[],'text':[]}
    for j,i in tweets.iterrows():
        temp['screenname']+=[i['user']['screen_name']]
        temp['text']+= [i['text']]
    df1 = pd.DataFrame(temp)
    
    result = df.merge(df1, on='screenname', how='inner')
    
    sent=[]
    for j,i in result.iterrows():
        sent+=[sentiment_scores(i['text'])]
    result['sentiment'] = sent
    
    overall={ 'pos':0,
          'neg':0,
          'neu':0}
    for i in result['sentiment']:
        if i>= 0.05 :
            overall['pos']+=1
    
        elif i <= - 0.05 :
            overall['neg']+=1
    
        else :
            overall['neu']+=1
        
    total_inf=sum(result['inf'])
    
    infl=[]
    for j,i in result.iterrows():
        infl+=[(i['inf']/total_inf)*100]
        
    result['Inf_percent']=infl
    
    
    poverall={ 'pos':0,
          'neg':0,
          'neu':0}
    for j,i in result.iterrows():
        if i['sentiment']>= 0.05 :
            poverall['pos']+=i['Inf_percent']
    
        elif i['sentiment'] <= - 0.05 :
            poverall['neg']+=i['Inf_percent']
    
        else :
            poverall['neu']+=i['Inf_percent']
            
    pos =[]
    neg = []
    neu = []
    for j,i in result.iterrows():
        sent=proposed_sent(i['text'])
        pos+=[sent['pos']]
        neg+=[sent['neg']]
        neu+=[sent['neu']]
    result['pos'] = pos
    result['neg'] = neg
    result['neu'] = neu
    return result
    
def proposed_sent(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict
    


def get_trends_india():
    
    consumer_key = 'Tm30Tmmk1eaEzbi23Nm3NU1g5'
    consumer_secret = 'jId4w7i1QLJGqv3JnlM33N9ZzZEhP1QmYu6RzaBYarrNM5HAzG'
    access_token = '1390534356796514304-5KUsYqQaXJXxKwauEupXT7UtkYLAmY'
    access_token_secret = 'U4nDzR99UsH8aCuKB9ntLGbZLCwwoDkLLjt0A3FvwngT1'

    # Authorization and Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api1 = tweepy.API(auth)
    trends = api1.get_place_trends(23424848)
    trends=trends[0]['trends']
    hashtag=[]
    vol=[]
    
    for i in trends:
      hashtag+=[i['name']]
      vol+=[i['tweet_volume']]
    
    return pd.DataFrame({'hashtag':hashtag, 'vol':vol}).dropna()

def summarize(text, size):
    nltk.download('punkt')
    nltk.download('stopwords')
    # Preprocessing the data
    text = re.sub(r'\[[0-9]*\]',' ',text)
    text = re.sub(r'(\@|\#)(\S)+(\b)',' ',text)
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text)
    text = re.sub(r'\s+',' ',text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W',' ',clean_text)
    clean_text = re.sub(r'\d',' ',clean_text)
    clean_text = re.sub(r'(\s)+',' ',clean_text)
    
    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)
    
    # Stopword list
    stop_words = nltk.corpus.stopwords.words('english')
    
    # Word counts 
    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    
    # Converting counts to weights
    for key in word2count.keys():
        word2count[key] = word2count[key]/max(word2count.values())
        
    # Product sentence scores    
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]
                        
    # Gettings best 5 lines             
    best_sentences = heapq.nlargest(size, sent2score, key=sent2score.get)
    
    summary = []
    for sentence in best_sentences:
        summary = summary + [sentence]
        #summary.append(sentence)
    
    return summary

def generate_sentiment_summary(df):
    pos_tweets = []
    neg_tweets = []
    for i, row in df.iterrows():
        if row['sentiment'] == 'Positive':
            pos_tweets.append(row['text'])
        elif row['sentiment'] == 'Negative':
            neg_tweets.append(row['text'])
        else:
            pass
    
    pos_text = (". ").join(pos_tweets)
    neg_text = (". ").join(neg_tweets)

    summary_size = int(pow(len(df),0.5))
    pos_summary = summarize(pos_text, summary_size)
    neg_summary = summarize(neg_text, summary_size)

    print('\nPositive: ')
    print(pos_summary)

    print('\nNegative: ')
    print(neg_summary)


def get_userdata(userID):
    
    api = tweepy.API(auth,timeout=10)
    timeline = api.home_timeline()
    
    tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=100,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        
    og_tweets = [i for i in all_tweets if not str(i.full_text).startswith('@')]
    og_tweets 
    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(og_tweets)]
    df = DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count","text"])
    df.to_csv('%s_tweets.csv' % userID,index=False)
    
    engagement = []
    for i,row in df.iterrows():
        engagement.append(row['favorite_count']+row['retweet_count'])

    df['engagement'] = engagement
    df1 = twitter_profile_query(userID)
    sentiment_polarity = []
    for j,i in df1.iterrows():
        if i['sentiment']>= 0.05 :
            sentiment_polarity.append('positive')
        elif i['sentiment'] <= - 0.05 :
            sentiment_polarity.append('negative')
        else :
            sentiment_polarity.append('neutral')

    df1['sentiment_polarity'] = sentiment_polarity
    
    results = api.get_user(screen_name=userID)

    no_ofFollowers = results.followers_count
    no_ofLikes = results.favourites_count
    no_ofFollowing = results.friends_count
    no_ofTweetsCount = results.statuses_count
    
    return df, df1, no_ofFollowers, no_ofLikes,no_ofFollowing, no_ofTweetsCount
    
def get_graphs(df,df1):
    if len(df)>100:
        l = 100
    else:
        l = len(df)
    sub_df = df[:l]
   
    fig0 = px.bar(sub_df, y=sub_df['favorite_count'], color=sub_df['favorite_count'], color_continuous_scale = "Spectral", template='plotly_white')
    fig0.write_html('./main/templates/main/favcount.html')
    fig1 = px.bar(sub_df, y=sub_df['retweet_count'], color=sub_df['retweet_count'], color_continuous_scale = "Spectral", template='plotly_white')
    fig1.write_html('./main/templates/main/rtcount.html')
    fig2 = px.line(sub_df, x='created_at', y='engagement', template='plotly_white')
    fig2.write_html('./main/templates/main/eng.html')
    fig = px.line(df1, x="date", y="sentiment", color='sentiment_polarity', color_discrete_sequence=["#686de0", "#6ab04c", "#ff7979"], markers=True, template='plotly_white')
    fig.write_html('./main/templates/main/sentcount.html')
    
    

