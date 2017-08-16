import requests
import json
from TwitterAPI import TwitterAPI
from datetime import datetime
import os
from rq import Queue

from worker import conn

BOTNAME = 'strictlyvote'
TEAMS = ['tmp1' ,'tmp2']

def vote_parse(user, text):
    for team in TEAMS:
        if text.find(team) != -1:
            log = "One vote for {} from {}".format(team,user)
            with open("test.txt", "a") as myfile:
                myfile.write(log)
            break
            print(log)
    return

def find_number(text):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

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
        job = q.enqueue(vote_parse, item['user']['screen_name'], item['text'])
    return

def strip_tag(text):
    if text.find('#'+BOTNAME) != -1:
        text = text.replace('#'+BOTNAME,'')
    elif text.find(BOTNAME) != -1:
        text = text.replace(BOTNAME,'')
    new_text = text.strip()
    return ' '.join(new_text.split()).replace(' ','+')



if __name__ == "__main__":
    # name = "M1"
    # resp = fetch_image(name)
    # if resp:
    #     print resp
    # else:
    #     print "Couldn't find %s" % name
    monitor('')
