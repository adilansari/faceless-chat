from flask import Flask, request
from mongokit import Connection, Document
from bson import ObjectId
import json
import time

app = Flask(__name__)
app.config.from_object(__name__)
DATABASE_NAME = 'chat'

db = Connection('localhost', 27030)


@db.register
class Users(Document):
    __database__ = DATABASE_NAME
    __collection__ = 'users'

    structure = {
        'record_id': ObjectId
    }

    use_dot_notation = True
    use_schemaless = False

    def create(self, record_id):
        self.record_id = ObjectId(record_id)
        self.save()
        return str(self._id)


@db.register
class Record(Document):
    __database__ = DATABASE_NAME
    __collection__ = 'records'

    structure = {
        'ip_addr': str,
        'referer': unicode,
        'user_agent': unicode,
        'created_at': int
    }
    use_dot_notation = True
    use_schemaless = False

    def create(self, data, ip_addr):
        self.ip_addr = ip_addr
        self.referer = data.get('Referer', None)
        self.user_agent = data.get('User-Agent', None)
        self.created_at = int(time.time())
        self.save()
        return str(self._id)


@app.route('/')
def home():
    return 'Use /pixel endpoint'


@app.route('/pixel')
def pixel():
    print 'pixel'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9898)
