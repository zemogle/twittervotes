import os
import redis
from worker import conn
from datetime import datetime

TEAMS = ['tmp1' ,'tmp2']
WEEKS = ['20170923']

def find_number(text):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

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

def scan_db():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    text = "<h1>{}</h1>".format(the_time)
    for key in conn.keys("scd:*"):
        line = conn.get(key)
        text += "<p>{} | {}</p>".format(key,line)

    return text
