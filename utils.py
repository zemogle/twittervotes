import os
import redis
from datetime import datetime
from rq import Queue
from TwitterAPI import TwitterAPI

from worker import conn

#from worker import conn

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
            if scores:
                users = conn.get(team_week_users)
                if not users or user not in users:
                    score = int(scores[0])
                    conn.incrby(team_week_score, score)
                    conn.append(team_week_users, "{};".format(user))
            break
    return
