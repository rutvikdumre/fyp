import instaloader

insta= instaloader.Instaloader()
username= 'sendmomo'


uids=['techcommmpstme', 'sportscommittee.mpstme', 'culturalcommittee_mpstme']
followers=[]
media=[]
for i in uids:
    profile=instaloader.Profile.from_username(insta.context, i)
    followers += [profile.followers]
    media += [profile.mediacount]
    


'''import numpy as np 
import matplotlib.pyplot as plt 
  
X = uids
Ygirls = followers
Zboys = media
  
X_axis = np.arange(len(X))
  
plt.bar(X_axis - 0.2, Ygirls, 0.4, label = 'Followers')
plt.bar(X_axis + 0.2, Zboys, 0.4, label = 'Media Count')
  
plt.xticks(X_axis, X)
plt.xlabel("Users")
plt.ylabel("Count")
plt.title("Competetive Comparision")
plt.legend()
plt.show()'''


#x=user.get_followers()

'''x=user.get_posts()
y= user.get_similar_accounts()

print('Similar Accounts:')
for i in y:
    print(i)

for i in x:
    for j in i.get_likes():
        print(j)
    print('------------')'''


for i in profile.get_posts():
    print(i.date) 
