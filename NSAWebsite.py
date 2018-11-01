# import sleep so we can wait between getting more tweets
from time import sleep

# load firestore credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
 
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)

# load collection
db = firestore.client()
nsaUpdates = db.collection(u'NSA Updates')

# import rss parser
import feedparser

# url to NSA RSS
nsa_rss = 'https://www.nsa.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=920&max=20'

# parse feed
feed = feedparser.parse( nsa_rss )

# package feed into update for firestore
update = {
            u'source': u'twitter',
            u'title': u'',
            u'body': tweet.text,
            u'time': str(tweet.created_at)
}

