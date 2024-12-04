import datetime
import logging
import time
import threading

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from turbo_flask import Turbo

turbo = Turbo()
bootstrap = Bootstrap()

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