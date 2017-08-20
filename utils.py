import tinys3, os
import redis
from worker import conn

TEAMS = ['tmp1' ,'tmp2']

def find_number(text):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

def vote_parse(user, text):
    for team in TEAMS:
        if text.find(team) != -1:
            log = "One vote for {} from {}".format(team,user)
            scores = find_number(text)
            if scores:
                score = int(scores[0])
                store_value(team, score)
            break
    return

def store_value(team, score):
    if team not in conn.keys():
        conn.incr(team, score)
    else:
        conn.set(team, score)

    return

def push_to_s3():
    conn = tinys3.Connection(os.environ['AWS_ACCESS_KEY_ID'],os.environ['AWS_SECRET_KEY'],tls=True)

    f = open('test.txt','rb')
    conn.upload('test.txt', f ,'darkmattersheep.uk/strictly/')
    return
