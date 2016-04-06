from flask import *
from pusher import Pusher
import time
import os

app = Flask(__name__)
app.config.from_object(__name__)
DATABASE_NAME = 'chat'

CHANNEL_NAME = 'notifications'
NOTIFICATION_EVENT_NAME = 'new_notification'

pusher = Pusher(
    app_id=os.environ['PUSHER_APP_ID'],
    key=os.environ['PUSHER_KEY'],
    secret=os.environ['PUSHER_SECRET']
)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('chat'))


@app.route('/chat')
def chat():
    return render_template(
        'chat.html',
        pusher_key=os.environ['PUSHER_KEY'],
        channel_name=CHANNEL_NAME,
        notification_event_name=NOTIFICATION_EVENT_NAME)


@app.route('/publish')
def pixel():
    print 'pixel'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
