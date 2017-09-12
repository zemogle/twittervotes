import requests
import json
from flask import Flask
import os
import redis
from datetime import datetime

from worker import conn

app = Flask(__name__)

TEAMS = ['tmp1' ,'tmp2']
WEEKS = ['20170923']

def scan_db():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    text = "<h1>{}</h1>".format(the_time)
    for key in conn.keys("scd:*"):
        line = conn.get(key)
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
