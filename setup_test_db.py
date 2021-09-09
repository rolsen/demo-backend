import datetime

import messenger

def setup_test_db():
    print("Creating db...")
    app = messenger.app
    db = messenger.db
    db.create_all()

    print("Inserting test data into db...")
    db.session.add(messenger.User(id=123))
    db.session.add(messenger.User(id=456))
    db.session.add(messenger.User(id=789))

    db.session.add(messenger.Message(id=1000, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 8, 8, 23, 59, 59),
        text="Old hello"))

    db.session.add(messenger.Message(id=1001, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 9, 8, 23, 59, 59),
        text="¡This is a Unicode message with 256 characters or less in it!"))

    db.session.add(messenger.Message(id=1002, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 9, 9, 8, 59, 59),
        text="Hello"))

    db.session.add(messenger.Message(id=1003, sender_id=456, recipient_id=123,
        datetime=datetime.datetime(2021, 9, 9, 8, 59, 59),
        text="Hello back"))

    db.session.add(messenger.Message(id=1004, sender_id=123, recipient_id=789,
        datetime=datetime.datetime(2021, 9, 9, 9, 59, 59),
        text="Hello other"))

    db.session.commit()

if __name__ == '__main__':
    setup_test_db()
