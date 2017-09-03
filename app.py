import requests
import json
from flask import Flask
import os
import redis
from datetime import datetime

app = Flask(__name__)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

rd = redis.from_url(redis_url)

TEAMS = ['tmp1' ,'tmp2']
WEEKS = ['20170923']

def scan_db():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    text = "<h1>{}</h1>".format(the_time)
    for key in rd.keys("scd:*"):
        line = rd.get(key)
        text += "<p>{} | {}</p>".format(key,line)

    return text

def find_number(text):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

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
