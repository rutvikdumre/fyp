from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import urllib, base64
from . import quantinsta
import instaloader
from . import twitter_functions

insta= instaloader.Instaloader()

# Create your views here.
def landing(request):
    if request.method=='POST':
        uid=request.POST.get('uid')
        return redirect(reverse_lazy(f"main:analytics-by-topic '{uid}'"))
    return render(request,'main/index.html',{})

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
    df,positive,negative,neutral = twitter_functions.twitter_query('covid')
    df=df.iloc[:,:]
    fig = twitter_functions.sentplot(df)

    rows=list(df.itertuples(index=False))

    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    return render(request,'main/analysis.html',{'graph':uri,'data':rows,'topic':topic,'pos':positive,'neg':negative,'neu':neutral})


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