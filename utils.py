import tinys3, os
import redis
from worker import conn

TEAMS = ['tmp1' ,'tmp2']

def find_number(text):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers

def vote_parse(user, text):
    '''
    Find what the score and to which team. Store it in Redis
    '''
    for team in TEAMS:
        if text.find(team) != -1:
            scores = find_number(text)
            if scores:
                score = int(scores[0])
                conn.incrby(team, score)
            break
    return

def push_to_s3():
    conn = tinys3.Connection(os.environ['AWS_ACCESS_KEY_ID'],os.environ['AWS_SECRET_KEY'],tls=True)

    f = open('test.txt','rb')
    conn.upload('test.txt', f ,'darkmattersheep.uk/strictly/')
    return
