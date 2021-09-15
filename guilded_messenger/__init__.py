import datetime
import json
import os

import flask

from .db import init_db, db_session
from .models import User, Message



# Helper functions / testing hooks

def post_message(session, data):
    # TODO: Resolve users via User.query to ensure they exist.

    message = Message(
        sender_id=data['sender-id'],
        recipient_id=data['recipient-id'],
        datetime=datetime.datetime.fromisoformat(data['datetime']),
        text=data['text'],
    )
    session.add(message)
    session.commit()
    return message.to_dict()


def create_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'guilded_messenger.sqlite'),
    )
    # TODO: Clean up
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_db()
    try:
        # Force an exception if the db isn't initialized
        User.query.filter_by().first()
    except Exception as e:
        print('[WARN] Database has no data, adding test data...')
        add_test_data()


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ########################################################################
        # Not happening
        ########################################################################
        print('shutdown_session')
        db_session.remove()


    # API

    @app.route("/messages.json", methods=['GET', 'POST'])
    def messages():
        if flask.request.method == 'POST':
            # KeyError raised by access method of flask.request.form will render a
            # 400 BAD REQUEST
            data = flask.request.json
            return json.dumps(post_message(db_session, data))
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
                oldest = datetime.datetime.utcnow() - datetime.timedelta(days=days)
                q = q.filter(Message.datetime > oldest)

            if params.get('count-limit', None) is not None:
                q = q.limit(int(params['count-limit']))

            msgs = q.all()
            result["count"] = len(msgs)
            for msg in msgs:
                result['messages'].append(msg.to_dict())

            return json.dumps(result)

    return app
