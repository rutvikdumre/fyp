import instaloader
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

insta= instaloader.Instaloader()
username= 'sendmomo'

def get_profileObject(username):
    '''
    Retrieve a profile object for a given username
    '''
    profile = instaloader.Profile.from_username(insta.context, username)
    return profile

def get_profileDetails(profile):
    followers = profile.followers
    media_count = profile.mediacount
    
def get_postDetails(profile):
    '''
    Retrieve attributes for all posts of a user
    profile - profile object for a particular user
    '''
    post_id, likes, comments, is_video, video_view_count, date = ([] for i in range(6)) # post_id - post shortcode
    for i in profile.get_posts():
        post_id.append(i.shortcode)
        likes.append(i.likes)
        comments.append(i.comments)
        is_video.append(i.is_video)
        video_view_count.append(i.video_view_count)
        date.append(i.date)

    post_df = pd.DataFrame(data={'id':post_id, 'likes':likes, 'comments':comments, 
                                'is_video':is_video, 'video_view_count':video_view_count,'upload_date':date})
    
    return post_df
        
def likesPerPost(df, username):
    
    # Create plot and style. 
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12,4))

    # Draw scatter plot.
    upload_date = df["upload_date"].to_numpy()
    likes = df["likes"].to_numpy()
    ax.scatter(upload_date, likes, label="Post")
    
    left_xlim=df["upload_date"].min()-datetime.timedelta(days=3)
    right_xlim=df["upload_date"].max()+datetime.timedelta(days=3)
    ax.set_xlim(left=left_xlim, right=right_xlim)
    
    # Draw labels on plot. 
    ax.set_title("{} Instagram Likes per Post".format(username))
    ax.set_xlabel("Date")
    ax.set_ylabel("Likes")
    
    return plt
    
def likesVsComments(post_df, username):
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(12,4), facecolor="w")
    ax.set_yscale('log')

    # Draw the plots 
    posts = [i for i in range(len(post_df))]
    likes = df['likes'].to_numpy()
    comments = df["comments"].to_numpy()
    ax.bar(posts, likes, label="Likes", width=1, color="#ff6b6b")
    ax.bar(posts, comments, label="Comments", width=1, color="#0abde3")

    # Draw the labels 
    ax.set_title("{} Instagram Likes vs. Comments per Post".format(username))
    ax.set_xlabel("Post")
    ax.set_ylabel("Instagram user")
    '''ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))'''
    ax.legend()
    plt.show()
    
def viewsVsLikes(post_df, username):
    
    # Create figure and set logarithmic y-axis
    videos_df = post_df[post_df["is_video"]]
    fig, ax = plt.subplots(figsize=(12,4), facecolor='w')
    ax.set_yscale('log')

    # Draw bar plots 
    posts = [i for i in range(len(videos_df))]
    view_count = videos_df['video_view_count'].to_numpy()
    likes = videos_df["likes"].to_numpy()
    ax.bar(posts, view_count, label="Views", color="#ff6b6b")
    ax.bar(posts, likes, label="Likes", color="#0abde3")

    # Draw labels 
    ax.set_title("{} Instagram Views and Likes per Video".format(username))
    ax.set_xlabel("Post")
    ax.set_ylabel("Instagram user")
    '''ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))'''
    ax.legend()
    return plt

def comp_followers(uids):
    # uids=['techcommmpstme', 'sportscommittee.mpstme', 'culturalcommittee_mpstme']
    followers=[]
    media=[]
    for i in uids:
        profile=instaloader.Profile.from_username(insta.context, i)
        followers += [profile.followers]
        #media += [profile.mediacount]
    X = uids
    Y = followers
    #Zboys = media

    X_axis = np.arange(len(X))

    plt.bar(X_axis , Y, label = 'Followers')
    #plt.bar(X_axis + 0.2, Zboys, 0.4, label = 'Media Count')

    plt.xticks(X_axis, X)
    plt.xlabel("Users")
    plt.ylabel("Count")
    plt.title("Competetive Comparision")
    plt.legend()
    # plt.show()
    return plt


profile_username = 'parvdave29'
profile = get_profileObject(profile_username)
df = get_postDetails(profile)
likesPerPost(df, profile_username)

