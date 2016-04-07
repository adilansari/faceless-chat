from flask import *
from pusher import Pusher
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.environ['FLASK_SECRET']
app.debug = True

CHANNEL_NAME = 'notifications'
NOTIFICATION_EVENT_NAME = 'new_notification'
LOGIN_EVENT_NAME = 'new_user'
LOGOUT_EVENT_NAME = 'user_left'


pusher = Pusher(
    app_id=os.environ['PUSHER_APP_ID'],
    key=os.environ['PUSHER_KEY'],
    secret=os.environ['PUSHER_SECRET']
)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    login_user(username)
    pusher.trigger(CHANNEL_NAME, LOGIN_EVENT_NAME, {'username': username, 'message': 'has joined the chat room'})
    return redirect(url_for('chat'))


@app.route('/chat')
def chat():
    if not is_logged_in():
        return redirect(url_for('index'))

    return render_template(
        'chat.html',
        username=get_username(),
        pusher_key=os.environ['PUSHER_KEY'],
        channel_name=CHANNEL_NAME,
        notification_event_name=NOTIFICATION_EVENT_NAME,
        login_event_name=LOGIN_EVENT_NAME,
        logout_event_name=LOGOUT_EVENT_NAME)


@app.route('/publish', methods=['POST'])
def publish():
    message = request.form['message']
    pusher.trigger(CHANNEL_NAME, NOTIFICATION_EVENT_NAME, {'username': get_username(), 'message': message})
    response = jsonify(message='Message sent')
    response.status_code = 200
    return response


@app.route('/logout', methods=['POST'])
def logout():
    username = get_username()
    logout_user()
    pusher.trigger(CHANNEL_NAME, LOGOUT_EVENT_NAME, {'username': username, 'message': 'has left the chat room'})
    return redirect(url_for('index'))


def is_logged_in():
    return 'username' in session


def get_username():
    return session['username']


def login_user(username):
    session['username'] = username


def logout_user():
    session.pop('username', None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
