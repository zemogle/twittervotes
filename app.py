import requests
import json
from flask import Flask, jsonify,json
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

@app.route("/results.json")
def get_results():
    
    try:

        # Initialize a employee list
        teams = []

        # create a instances for filling up employee list
        for key in conn.keys("scd:*"):
            teams = {
               'score': conn.get(key),
               'team': key}
            teams.append(scores)
    
        # convert to json data
        jsonStr = json.dumps(teams)

    except Exception ,e:
        print str(e)

    return jsonify(scores=jsonStr, timestamp=datetime.now().isoformat())



@app.route('/')
def homepage():
    return scan_db()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
