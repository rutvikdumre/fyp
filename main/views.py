from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import matplotlib.pyplot as plt
import io
import urllib, base64
from . import quantinsta
from . import twitter_functions
from .models import *
from .forms import RegisterForm
import instaloader


insta= instaloader.Instaloader()

# Create your views here.

def landing(request): # Landing Page View
    if request.user.is_authenticated:
        if request.method=='POST':
            uid=request.POST.get('uid')
            # print(user_history)
            return redirect('topic/'+uid)
        return render(request,'main/index.html',{})
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
    
    profile=instaloader.Profile.from_username(insta.context, username)
    # fig = quantinsta.comp_followers([username])
    # buf = io.BytesIO()
    # fig.savefig(buf,format='png')
    # buf.seek(0)
    # string = base64.b64encode(buf.read())
    # uri =  urllib.parse.quote(string)
    modes = {'likesperpost':{'name':'Likes per post'},'viewsvslikes':{'name':'Views vs Likes'},'compfollowers':{'name':'Followers comparison'}}
    return render(request,'main/options.html',{'profile':profile,'username':username,'modes':modes})

def analytics_by_topic(request,topic):
    twitter_functions.twitter_credentials()
    df,positive,negative,neutral = twitter_functions.twitter_query(topic)
    df=df.iloc[:,:]
    fig = twitter_functions.sentplot(df)

    rows=list(df.itertuples(index=False))

    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    #wordcloud
    fig = twitter_functions.wordcloud(twitter_functions.tweetClean(df))

    rows=list(df.itertuples(index=False))

    buf1 = io.BytesIO()
    fig.savefig(buf1,format='png')
    buf1.seek(0)
    string1 = base64.b64encode(buf1.read())
    uri1 =  urllib.parse.quote(string1)

    return render(request,'main/analysis.html',{'graph':uri,'wordcloud': uri1,'data':rows,'topic':topic,'pos':positive,'neg':negative,'neu':neutral})


def likes_per_post(request,username,mode):
    profile = quantinsta.get_profileObject(username)
    df = quantinsta.get_postDetails(profile)

    if mode == 'likesperpost':
        fig = quantinsta.likesPerPost(df, username)
    elif mode == 'viewsvslikes':
        fig = quantinsta.viewsVsLikes(df, username)
    elif mode == 'compfollowers':
        fig = quantinsta.comp_followers([username])
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    return render(request,'main/analysis.html',{'data':uri,'username':username})

# likesPerPost
# viewsvslikes
# comp_followers