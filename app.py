import datetime
import logging
import time
import threading
import redis

import constants

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from turbo_flask import Turbo

turbo = Turbo()
bootstrap = Bootstrap()
rc = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)
    turbo.init_app(app)
    return app

app = create_app()
app.config['SERVER_NAME'] = '127.0.0.1:8080'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/movies")
def movies():
    return render_template('index.html')

@app.route("/television")
def television():
    return render_template('index.html')

@app.route("/music")
def music():
    return render_template('index.html')

@app.route("/settings")
def settings():
    return render_template('index.html')