from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import matplotlib.pyplot as plt
import io
import urllib, base64
from . import quantinsta
from . import twitter_functions
from .models import *
from .forms import RegisterForm
from django.template.loader import render_to_string, get_template
from . import hashtag 


# Create your views here.

def landing(request): # Landing Page View
    if request.user.is_authenticated:
        if request.method=='POST':
            uid=request.POST.get('uid')
            # print(user_history)
            return redirect('topic/'+uid)
        
        br = render_to_string('main/file.html')
        return render(request,'main/index.html',{'br':br})
    else:
        return redirect('main:login-view')

def register(response):
    if response.method=='POST':
        form=RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('main:landing-page')
    else:
        form=RegisterForm()
    return render(response, "main/register.html", {'form':form})



def analytics_by_account(request,username):
    
    
    modes = {'likesperpost':{'name':'Likes per post'},'viewsvslikes':{'name':'Views vs Likes'},'compfollowers':{'name':'Followers comparison'}}
    return render(request,'main/options.html',{'profile':profile,'username':username,'modes':modes})

def analytics_by_topic(request):
    if request.method=="POST":
        topic=request.POST.get('topic')
        twitter_functions.twitter_credentials()
        df,positive,negative,neutral = twitter_functions.twitter_query(topic)
        df=df.iloc[:,:]
        twitter_functions.sentplot(df)

        rows=list(df.itertuples(index=False))

        """buf = io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri =  urllib.parse.quote(string)"""

        sent = render_to_string('main/sent.html')

        #wordcloud
        fig = twitter_functions.wordcloud(twitter_functions.tweetClean(df))

        rows=list(df.itertuples(index=False))

        buf1 = io.BytesIO()
        fig.savefig(buf1,format='png')
        buf1.seek(0)
        string1 = base64.b64encode(buf1.read())
        uri1 =  urllib.parse.quote(string1)

        return render(request,'main/analysis.html',{'sent':sent, 'wordcloud': uri1,'data':rows,'topic':topic,'pos':positive,'neg':negative,'neu':neutral})
    return render(request, "main/sentiment.html")

def compete(request):
    if request.method=='POST':
        uid=request.POST.get('uid')
        twitter_functions.score_compare(uid.split(","))
        inf = render_to_string('main/inf.html')
        reach = render_to_string('main/reach.html')
        pop = render_to_string('main/pop.html')
        likes = render_to_string('main/likes.html')
        return render(request, "main/user_comp.html", {'pop': pop, 'reach': reach, 'inf':inf, 'likes':likes} )
    return render(request, "main/user_input.html")

def gethastag(request):
    if request.method=='POST':
        content=request.POST.get('content')
        hashtags= hashtag.gethash(content)
        #print(hashtags)
        data= twitter_functions.get_trends_india()
        return render(request, "main/showhash.html", {'hashtags': " ".join(hashtags), 'content':content, 'data':data} )
    return render(request, "main/gethashtags.html")


# likesPerPost
# viewsvslikes
# comp_followers