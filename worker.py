import os

from TwitterAPI import TwitterAPI
import redis
from rq import Worker, Queue, Connection

from utils import vote_parse

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

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

if __name__ == '__main__':
    monitor('')
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
