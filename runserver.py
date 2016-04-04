from flask import Flask, render_template
from pusher import Pusher
import time
import os

app = Flask(__name__)
app.config.from_object(__name__)
DATABASE_NAME = 'chat'

CHANNEL_NAME = 'soccer'

pusher = Pusher(
    app_id=os.environ['PUSHER_APP_ID'],
    key=os.environ['PUSHER_KEY'],
    secret=os.environ['PUSHER_SECRET']
)


@app.route('/')
def home():
    return render_template('home.html', pusher_app=os.environ['PUSHER_APP_ID'])


@app.route('/pixel')
def pixel():
    print 'pixel'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
