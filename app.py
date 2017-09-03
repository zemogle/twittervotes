import requests
import json
from TwitterAPI import TwitterAPI
from flask import Flask
import os
from rq import Queue

from worker import conn
from utils import vote_parse, scan_db

app = Flask(__name__)
BOTNAME = 'strictlyvote'

def monitor(search_terms):
    read = False
    q = Queue(connection=conn)
    api = TwitterAPI(
                os.environ.get('BOT_CONSUMER_KEY', ''),
                os.environ.get('BOT_CONSUMER_SECRET', ''),
                os.environ.get('BOT_ACCESS_KEY', ''),
                os.environ.get('BOT_ACCESS_SECRET', ''),
            )

    openstream = api.request('statuses/filter', {'track': BOTNAME})
    for item in openstream:
        job = q.enqueue(vote_parse, item['user']['screen_name'], item['text'])
    return

def strip_tag(text):
    if text.find('#'+BOTNAME) != -1:
        text = text.replace('#'+BOTNAME,'')
    elif text.find(BOTNAME) != -1:
        text = text.replace(BOTNAME,'')
    new_text = text.strip()
    return ' '.join(new_text.split()).replace(' ','+')

@app.route('/')
def homepage():
    return scan_db()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    monitor('')
