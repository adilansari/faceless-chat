from flask import Flask, request
from bson import ObjectId
import json
import time

app = Flask(__name__)
app.config.from_object(__name__)
DATABASE_NAME = 'chat'


@app.route('/')
def home():
    return 'Use /pixel endpoint'


@app.route('/pixel')
def pixel():
    print 'pixel'

