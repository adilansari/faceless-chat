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
    app_id=os.environ.get('PUSHER_APP_ID', '194612'),
    key=os.environ.get('PUSHER_KEY', 'f4ee88e008548564dbc5'),
    secret=os.environ.get('PUSHER_SECRET', '920f9448c42e8ff5c49c')
)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    print 'logging in {}'.format(username)
    return redirect(url_for('chat'))


@app.route('/chat')
def chat():
    return render_template(
        'chat.html',
        pusher_key=os.environ.get('PUSHER_KEY', 'f4ee88e008548564dbc5'),
        channel_name=CHANNEL_NAME,
        notification_event_name=NOTIFICATION_EVENT_NAME)


@app.route('/publish', methods=['POST'])
def publish():
    message = request.form['message']
    pusher.trigger(CHANNEL_NAME, NOTIFICATION_EVENT_NAME, {'message': message})
    response = jsonify(message='Message sent')
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
