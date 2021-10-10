import os 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#CSy9g1KDimx - Parv techcom
#CTEnZXbNsJ7 - Sportscom

'''
os.system('instaloader --comments -- -CSy9g1KDimx')
os.system('instaloader --comments -- -CTEnZXbNsJ7')'''
def sentiment_scores(sentence):
  
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
  
    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    return sentiment_dict['compound']

      
import json

def jsontolist(name):
    # Load credentials from json file
    with open(name, "r") as file:
        creds = json.load(file)
    l=[]
    for i in creds:
        l+=[i['text']]
    return l


l= jsontolist(r"-CSy9g1KDimx\2021-08-20_12-30-06_UTC_comments.json")
sum=0
for i in l:
    sum+=sentiment_scores(i)
techcom= sum/len(l)


l= jsontolist(r"-CTEnZXbNsJ7\2021-08-27_09-03-10_UTC_comments.json")
sum=0
for i in l:
    sum+=sentiment_scores(i)
sportscom= sum/len(l)

print('AVG sentiment score for Techcom: {} \nAVG sentiment score for Sportscom: {}'.format(techcom,sportscom))









from nltk import tokenize
from operator import itemgetter
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 


def check_sent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

def keywords(doc,n):
  nltk.download('stopwords')
  nltk.download('punkt')
  stop_words = set(stopwords.words('english'))
  total_words = doc.split()
  total_word_length = len(total_words)
  #print(total_word_length)
  total_sentences = tokenize.sent_tokenize(doc)
  total_sent_len = len(total_sentences)
  #print(total_sent_len)
  tf_score = {}
  for each_word in total_words:
      each_word = each_word.replace('.','')
      if each_word not in stop_words:
          if each_word in tf_score:
              tf_score[each_word] += 1
          else:
              tf_score[each_word] = 1

  # Dividing by total_word_length for each dictionary element
  tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
  #print(tf_score)
  idf_score = {}
  for each_word in total_words:
      each_word = each_word.replace('.','')
      if each_word not in stop_words:
          if each_word in idf_score:
              idf_score[each_word] = check_sent(each_word, total_sentences)
          else:
              idf_score[each_word] = 1

  # Performing a log and divide
  idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

  #print(idf_score)
  tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
  #print(tf_idf_score)
  result=''
  for i in get_top_n(tf_idf_score, n).keys():
    result+=str(i)+','
  #print(result[:-1])
  return result[:-1]

def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result
listToStr = ' '.join([str(elem) for elem in l])

ans=keywords(str(listToStr),20)
print("Keywords:")
print(ans)


print(sentiment_scores('this post is very bad'))
print(sentiment_scores('this product was not up to the mark'))
print(sentiment_scores('this is very boring'))
print(sentiment_scores('sun rise was at 6 oclock'))
print(sentiment_scores('The post is really helpful'))


