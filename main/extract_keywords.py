from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk


def generateKeyword(tweet):

    hashtags = set()
    words = word_tokenize(tweet)
    word_tokens = [word for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    keywords = []

    for word in word_tokens:
        if word not in stop_words:
            keywords.append(word)
    tagged_words = nltk.pos_tag(keywords)
    grammer = "NNP NNS NN VBG VB VBD VBN VBP NNPS JJ"

    for word in tagged_words:
        if (word[1] in grammer):
            hashtags.add(word[0])


    print('-------------')
    print('keywords: ',hashtags)
    return hashtags
