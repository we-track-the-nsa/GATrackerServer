# import sleep so we can wait between getting more tweets
from time import sleep

# import twitter handles that we pull from
f = open("Twitter_Accounts","r")

# break file into tokens signifiying a twitter handle
if f.mode == "r":
    contents = f.read().splitlines()

# load firestore credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
 
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)

# load twitter credentials

import tweepy
from tweepy import OAuthHandler

consumer_key = '8P1g6aWDGVGWTM0nRv77w52V5'
consumer_secret = 'O8WE0S6a18FXK5dG8O2I8XP2oHh7c0EOnZEaIF4LVwgIn6dXhV'
access_token = '1057334387862310912-3VMoUqyq3rhAJ7KctD1HaeUDCF2xKK'
access_secret = 'v0Fg9nxSdZGnlDEa02U3Lh7DCIjwYiIwPiRyqbOYC6zfb'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

while(1):
    for content in contents:
        # load collection
        db = firestore.client()
        col = db.collection(content + u' Updates')
        col_all = db.collection('All Updates')

        # get posts from twitter
        posts = api.user_timeline(screen_name = content, count = 20, include_rts = True)
        print 'reading and uploading posts from: ' + content
        for tweet in posts:
            # package tweet from twitter into update format for firebase
            update = {
                u'source': u'twitter',
                u'title': u'',
                u'body': unicode(tweet.text),
                u'time': unicode(str(tweet.created_at))
            }
            update_all = {
                u'source': u'twitter',
                u'title': u'',
                u'body': unicode(tweet.text),
                u'time': unicode(str(tweet.created_at)),
                u'agency': unicode(content)
            }
            # print update
            # print update_all
            #print tweet.created_at
            # add udpate to firestore collection
            col.document(str(tweet.created_at)).set(update)
            col_all.document(str(tweet.created_at)).set(update_all)

    print 'sleeping.......'
    sleep(60 * 15) # 15 min = 15 * 60 secs