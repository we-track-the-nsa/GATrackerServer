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

def monthToNum(month):
    if 'Jan' in month:
        return 1
    elif 'Feb' in month:
        return 2
    elif 'Mar' in month:
        return 3
    elif 'Apr' in month:
        return 4
    elif 'May' in month:
        return 5
    elif 'Jun' in month:
        return 6
    elif 'Jul' in month:
        return 7
    elif 'Aug' in month:
        return 8
    elif 'Sep' in month:
        return 9
    elif 'Oct' in month:
        return 10
    elif 'Nov' in month:
        return 11
    elif 'Dec' in month:
        return 12
    else:
        return -1

while(1):
    for content in contents:
        parsed = feedparser.parse(content)
        agency = ''
        if 'cia.gov' in content:
            agency = 'CIA'
        elif 'dod.defense.gov' in content:
            agency = 'DeptofDefense'
        elif 'nsa.gov' in content:
            agency = 'NSAGov'
        elif 'fbi.gov' in content:
            agency = 'FBI'
        elif 'justice.gov' in content:
            agency = 'TheJusticeDept'
        else:
            agency = 'unknown'

        # TODO check if could be other agencies

        # load collection
        db = firestore.client()
        col = db.collection(agency + u' Updates')
        col_all = db.collection('All Updates')

        print 'reading and uploading posts from: ' + agency
        for entry in parsed['entries']:
            # print entry
            # package tweet from twitter into update format for firebase
            time = entry['updated']
            if agency == 'CIA' or agency == 'FBI':
                temp = time[:10] + ' ' + time[11:19]
                time = temp
            elif agency == 'DeptofDefense' or agency == 'NSAGov' or agency == 'TheJusticeDept':
                monthNum = monthToNum(time[8:11])
                temp = time[12:16] + '-' + str(monthNum).zfill(2) + '-' + time[5:7] + ' ' + time[17:25]
                time = temp
                
            update = {
                u'source': u'website',
                u'title': unicode(entry['title']),
                u'body': unicode(entry['summary']),
                u'time': unicode(time)
            }
            # update_all = {
            #     u'source': u'website',
            #     u'title': unicode(entry['title']),
            #     u'body': unicode(entry['summary']),
            #     u'time': unicode(time),
            #     u'agency': unicode(agency)
            # }
            # print agency
            # print time
            
            # add udpate to firestore collection
            col.document(time).set(update)
            # col_all.document(entry['updated']).set(update_all)

    print 'sleeping.......'
    sleep(60 * 15) # 15 min = 15 * 60 secs
