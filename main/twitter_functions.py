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
      
    '''print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
  
    print("Sentence Overall Rated As", end = " ")'''
  
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return "Positive"
  
    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"
  
    else :
        return "Neutral"

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

    # Create our query
    query = {'q': query,
            'result_type': 'mixed',
            'count': 100,
            'lang': 'en',
            'geocode':'' 
            }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'hashtags':[], 'location':[]}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])
        dict_['hashtags'].append([hashtag['text'] for hashtag in status['entities']['hashtags']])
        dict_['location'].append(status['user']['location'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    sentiment=[]
    for i in df['text']:
        sentiment+=[sentiment_scores(i)]
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
    fig, ax = plt.subplots()
    color_dict = {'Positive':'#6ab04c', 'Negative':'#eb4d4b', 'Neutral':'#22a6b3'}
    fig=df['sentiment'].value_counts().plot(ax=ax, kind='barh',color=df['sentiment'].replace(color_dict))
    return plt

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


    print(df_tweets.head)
    pd.options.plotting.backend = "plotly"


    # Likes
    


    fig0 = go.Figure(data=[go.Pie(labels=df_tweets['screenname'], values=df_tweets['no_of_likes'], hole=.3)])

    fig0.write_html('./main/templates/main/likes.html')


    # Popularity Score and Reach score

    fig1=df_tweets.plot.bar(y='screenname', x="popularity_score")
    fig1.write_html("./main/templates/main/pop.html")

    fig2 = df_tweets.plot.bar(y='screenname', x="reach_score")
    fig2.write_html("./main/templates/main/reach.html")

    # Normalisation and Influencer score calculation

    scaler = MinMaxScaler(feature_range=(0,1))
    df_tweets[['popularity_score', 'reach_score']]= scaler.fit_transform(df_tweets[['popularity_score', 'reach_score']])

    inf=[]
    for index, i in df_tweets.iterrows():
      inf+=[inf_calc_users(i['popularity_score'],i['reach_score'])]
    df_tweets['inf']=inf


    print(df_tweets.head)


    fig3 = df_tweets.plot.bar(y='screenname', x="inf")
    fig3.write_html("./main/templates/main/inf.html")
            