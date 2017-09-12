import requests
import json
from flask import Flask
import os
import redis
from datetime import datetime

from worker import conn

app = Flask(__name__)


def scan_db():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    text = "<h1>{}</h1>".format(the_time)
    for key in conn.keys("scd:*"):
        line = conn.get(key)
        text += "<p>{} | {}</p>".format(key,line)

    return text




@app.route('/')
def homepage():
    return scan_db()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
