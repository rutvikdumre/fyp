import tweepy

consumer_key = 'Tm30Tmmk1eaEzbi23Nm3NU1g5'
consumer_key_secret = 'jId4w7i1QLJGqv3JnlM33N9ZzZEhP1QmYu6RzaBYarrNM5HAzG'
access_token = '1390534356796514304-5KUsYqQaXJXxKwauEupXT7UtkYLAmY'
access_token_secret = 'U4nDzR99UsH8aCuKB9ntLGbZLCwwoDkLLjt0A3FvwngT1'

def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
