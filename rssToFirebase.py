import feedparser

# import sleep so we can wait between getting more tweets
from time import sleep

# import twitter handles that we pull from
f = open("rss_url","r")

# break file into tokens signifiying a twitter handle
if f.mode == "r":
    contents = f.read().splitlines()

# load firestore credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
 
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)

while(1):
    for content in contents:
        parsed = feedparser.parse(content)
        print parsed['feed']['subtitle']
        print content
        print '\n'
        agency = ''
        if 'CIA' in parsed['feed']['subtitle']:
            agency = 'CIA'
        elif 'DoD' in parsed['feed']['subtitle']:
            agency = 'DeptofDefense'
        elif 'National Security Agency' in parsed['feed']['subtitle']:
            agency = 'NSAGov'
        elif 'National Press Releases' in parsed['feed']['subtitle']:
            agency = 'FBI'
        else:
            agency = 'TheJusticeDept'

        # TODO check if could be other agencies

        # load collection
        db = firestore.client()
        col = db.collection(agency + u' Updates')
        col_all = db.collection('All Updates')

        print 'printing and uploading posts from: ' + content
        for entry in parsed['entries']:
            print entry
            # package tweet from twitter into update format for firebase
            update = {
                u'source': u'website',
                u'title': unicode(entry['title']),
                u'body': unicode(entry['summary']),
                u'time': unicode(entry['updated'])
            }
            update_all = {
                u'source': u'website',
                u'title': unicode(entry['title']),
                u'body': unicode(entry['summary']),
                u'time': unicode(entry['updated']),
                u'agency': unicode(agency)
            }
            print update
            print update_all

            # add udpate to firestore collection
            col.document(entry['updated']).set(update)
            col_all.document(entry['updated']).set(update_all)

    print 'sleeping.......'
    sleep(60 * 15) # 15 min = 15 * 60 secs
