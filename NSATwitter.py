# load firestore credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
 
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)

# load collection
db = firestore.client()
nsaUpdates = db.collection(u'NSA Updates')

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

# get posts from twitter
nsaPosts = api.user_timeline(screen_name = 'NSAGov', count = 100, include_rts = True)

for tweet in nsaPosts:
    # package tweet from twitter into update format for firebase
    update = {
        u'source': u'twitter',
        u'title': u'',
        u'body': tweet.text,
        u'time': str(tweet.created_at)
    }
    print update

    # add udpate to firestore collection
    nsaUpdates.document(str(tweet.created_at)).set(update)