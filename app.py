import requests
import json
from TwitterAPI import TwitterAPI
from datetime import datetime
import os

# app = Celery('lcobot')
# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

IMG_URL = "http://data.lcogt.net/thumbnail"
BOTNAME = 'asklcobot'


def framedb_lookup(query):
    try:
        client = requests.session()

        # First have to authenticate
        login_data = dict(username='dthomas+guest@lcogt.net', password='guest')
        # Because we are sending log in details it has to go over SSL
        data_url = 'https://data.lcogt.net%s' % query
        resp = client.post(data_url, data=login_data, timeout=20)
        data = resp.json()
    except Exception, e:
        print e
        return False
    return data


def fetch_image(name):
    query = "/find?object_name=%s&limit=1&order_by=-date_obs&full_header=1" % name
    json_images = framedb_lookup(query)
    if json_images:
        img_file = json_images[0]['origname'][:-5]
        image = "%s/%s/?width=500&height=500&label=0" % (IMG_URL,img_file)
        obsdate = datetime.strptime(json_images[0]['date_obs'],"%Y-%m-%d %H:%M:%S")
        return json_images[0]['object_name'], json_images[0]['site'], obsdate.strftime("%-d %b %Y"), image
    else:
        return None

def monitor(search_terms):
    read = False
    api = TwitterAPI(
                os.environ.get('BOT_CONSUMER_KEY', ''),
                os.environ.get('BOT_CONSUMER_SECRET', ''),
                os.environ.get('BOT_ACCESS_KEY', ''),
                os.environ.get('BOT_ACCESS_SECRET', ''),
            )

    openstream = api.request('statuses/filter', {'track': BOTNAME})
    for item in openstream:
        try:
            tw_resp = tweet_decider(item['user']['screen_name'], item['text'])
            if tw_resp:
                r = api.request('statuses/update', {'status':tw_resp})
                print tw_resp
            else:
                print "Problem from %s" % item['user']['screen_name']
        except Exception, e:
            print(e,item)

def strip_tag(text):
    if text.find('#'+BOTNAME) != -1:
        text = text.replace('#'+BOTNAME,'')
    elif text.find(BOTNAME) != -1:
        text = text.replace(BOTNAME,'')
    new_text = text.strip()
    return ' '.join(new_text.split()).replace(' ','+')

def tweet_decider(user, text):
    text = strip_tag(text)
    if text:
        resp = fetch_image(text)
    if resp:
        tweet_text = "@%s Latest image of %s from %s on %s: %s" % (user, resp[0], resp[1], resp[2], resp[3])
    else:
        tweet_text = "@%s We didn't find %s sorry" % (user, text)
    return tweet_text



if __name__ == "__main__":
    # name = "M1"
    # resp = fetch_image(name)
    # if resp:
    #     print resp
    # else:
    #     print "Couldn't find %s" % name
    monitor('')
