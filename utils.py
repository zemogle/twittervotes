import os
import redis
from datetime import datetime
from rq import Queue
from TwitterAPI import TwitterAPI

from worker import conn


BOTNAME = 'strictlyvote'
WEEKS = ['20170923']
TEAMS = ['tmp1' ,'tmp2']

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

def show_db_vals():
    text = ''
    for key in conn.keys("scd:*"):
        line = conn.get(key)
        text += "{} | {}\n".format(key,line)
    print(text)
    return
    

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
        print("Found {} by {}".format(item['text'], item['user']['screen_name']))
        job = q.enqueue(vote_parse, item['user']['screen_name'], item['text'])
    return

def vote_parse(user, text):
    '''
    Find what the score and to which team. Store it in Redis
    '''
    currentweek = WEEKS[0]
    for team in TEAMS:
        if text.find(team) != -1:
            scores = find_number(text)
            team_week_score = "scd:{}-{}-score".format(team,currentweek)
            team_week_users = "scd:{}-{}-users".format(team,currentweek)
            print(scores)
            if scores:
                users = conn.get(team_week_users)
                print(users)
                if not users:# or user not in users:
                    score = int(scores[0])
                    conn.incrby(team_week_score, score)
                    conn.append(team_week_users, "{};".format(user))
            break
    show_db_vals()
    return
