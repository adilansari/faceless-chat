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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
