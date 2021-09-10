from datetime import datetime, timedelta
import json

import flask
from flask_sqlalchemy import SQLAlchemy


# Config

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Models

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime())
    text = db.Column(db.Unicode(256))

    def to_dict(self):
        return {
            'id': self.id,
            'sender-id': self.sender_id,
            'recipient-id': self.recipient_id,
            'datetime': self.datetime.isoformat(),
            'text': self.text,
        }


# Setup db

try:
    # Force an exception if the db isn't initialized
    User.query.filter_by().first()
except Exception as e:
    print('[ERR] Database not initialized, please run `setup_test_db.py`.')


# Helper functions / testing hooks


def post_message(data):
    # TODO: Resolve users via User.query to ensure they exist.

    message = Message(
        sender_id=data['sender-id'],
        recipient_id=data['recipient-id'],
        datetime=datetime.fromisoformat(data['datetime']),
        text=data['text'],
    )
    db.session.add(message)
    db.session.commit()
    return message.to_dict()


# API

@app.route("/messages.json", methods=['GET', 'POST'])
def messages():
    if flask.request.method == 'POST':
        # KeyError raised by access method of flask.request.form will render a
        # 400 BAD REQUEST
        data = flask.request.json
        return json.dumps(post_message(data))
    else:
        params = flask.request.args
        result = {
            "count": 0,
            "messages": [],
        }
        q = Message.query.order_by(Message.datetime.desc())

        if params.get('recipient-id', None) is not None:
            q = q.filter(Message.recipient_id == int(params['recipient-id']))

        if params.get('sender-id', None) is not None:
            q = q.filter(Message.sender_id == int(params['sender-id']))

        if params.get('day-limit', None) is not None:
            days = int(params['day-limit']) if (int(params['day-limit']) < 30) else 30
            oldest = datetime.utcnow() - timedelta(days=days)
            q = q.filter(Message.datetime > oldest)

        if params.get('count-limit', None) is not None:
            q = q.limit(int(params['count-limit']))

        msgs = q.all()
        result["count"] = len(msgs)
        for msg in msgs:
            result['messages'].append(msg.to_dict())

        return json.dumps(result)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
