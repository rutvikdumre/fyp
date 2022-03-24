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
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 


# Create your views here.

def login(request): # Landing Page View
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
    return render(response, "main/register1.html", {'form':form})



def analytics_by_account(request,username):
    modes = {'likesperpost':{'name':'Likes per post'},'viewsvslikes':{'name':'Views vs Likes'},'compfollowers':{'name':'Followers comparison'}}
    return render(request,'main/options.html',{'profile':profile,'username':username,'modes':modes})

def analytics_by_topic(request):
    if request.method=="POST":
        s=str(request.POST.get('topic'))
        return redirect('/sentiment/{}'.format(s))
    return render(request, "main/sentiment.html")

def sentimentfilter(request, topic):
    if request.method=="POST":
        twitter_functions.twitter_credentials()
        df,positive,negative,neutral = twitter_functions.twitter_query(topic)
        df=df.iloc[:,:]
        twitter_functions.sentplot(df)
        s=str(request.POST.get('Sentiment'))
        msg= ''
        if(s!='All' and s!='None'):
            df = df[df['sentiment'] == s]
            msg= ' [Showing data of only {} sentiment]'.format(s)

        rows=list(df.itertuples(index=False))
        text= ''
        for i in df['text']:
            text+='. '+ str(i)
      
        summary = twitter_functions.summarize(text, 5)

        sent = render_to_string('main/sent.html')

        #wordcloud
        fig = twitter_functions.wordcloud(twitter_functions.tweetClean(df))

        rows=list(df.itertuples(index=False))
        
        buf1 = io.BytesIO()
        fig.savefig(buf1,format='png')
        buf1.seek(0)
        string1 = base64.b64encode(buf1.read())
        uri1 =  urllib.parse.quote(string1)

        return render(request,'main/analysis.html',{'sent':sent, 'wordcloud': uri1,'data':rows,'topic':topic+msg,'pos':positive,'neg':negative,'neu':neutral, 'summary':summary})
    twitter_functions.twitter_credentials()
    df,positive,negative,neutral = twitter_functions.twitter_query(topic)
    df=df.iloc[:,:]
    twitter_functions.sentplot(df)

    rows=list(df.itertuples(index=False))
    sent = render_to_string('main/sent.html')
    #wordcloud
    fig = twitter_functions.wordcloud(twitter_functions.tweetClean(df))

    rows=list(df.itertuples(index=False))
    text= ''
    for i in df['text']:
        text+='. '+ str(i)
      
    summary = twitter_functions.summarize(text, 5)
    buf1 = io.BytesIO()
    fig.savefig(buf1,format='png')
    buf1.seek(0)
    string1 = base64.b64encode(buf1.read())
    uri1 =  urllib.parse.quote(string1)

    return render(request,'main/analysis.html',{'summary':summary,'sent':sent, 'wordcloud': uri1,'data':rows,'topic':topic,'pos':positive,'neg':negative,'neu':neutral})

def compete(request):
    if request.method=='POST':
        uid=request.POST.get('uid')
        tweet,fol,like,infc=twitter_functions.score_compare(uid.split(","))
        inf = render_to_string('main/inf.html')
        reach = render_to_string('main/reach.html')
        pop = render_to_string('main/pop.html')
        likes = render_to_string('main/likes.html')
        followers = render_to_string('main/followers.html')
        return render(request, "main/user_comp.html", {'uid':uid, 'pop': pop, 'reach': reach, 'inf':inf, 'likes':likes, 'followers':followers,
                                                       'tname':tweet['screenname'].to_string()[1:], 'tcount':tweet['tweet_count'].to_string()[1:], 
                                                       'fname':fol['screenname'].to_string()[1:], 'fcount':fol['no_of_followers'].to_string()[1:], 
                                                       'lname':like['screenname'].to_string()[1:], 'lcount':like['no_of_likes'].to_string()[1:], 
                                                       'iname':infc['screenname'].to_string()[1:], 'icount':infc['inf'].to_string()[1:]} )
    return render(request, "main/user_input.html")

def gethastag(request):
    if request.method=='POST':
        content=request.POST.get('content')
        hashtags= hashtag.gethash(content)
        #print(hashtags)
        
        return render(request, "main/showhash.html", {'hashtags': " ".join(hashtags), 'content':content} )
    data= twitter_functions.get_trends_india()
    data = list(data.itertuples(index=False))
    return render(request, "main/gethashtags.html",{'data':data})

def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None
 
def profile(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            tid=request.POST.get('tid')
            request.user.first_name =tid
            request.user.save()
            return render(request, "main/profile.html", {'msg':'Profile Updated Successfully!'})
        return render(request, "main/profile.html")
    return render(request, "main/profile.html")


def landing(request):
    return render(request, "main/landing.html")