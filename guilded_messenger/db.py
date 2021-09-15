import click
from flask.cli import with_appcontext
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:////tmp/test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    from .models import Base
    Base.query = db_session.query_property()


def add_test_data():
    from .models import Base
    print("Creating db...")
    Base.metadata.create_all(bind=engine)

    print("Inserting test data into db...")
    db_session.add(messenger.User(id=123))
    db_session.add(messenger.User(id=456))
    db_session.add(messenger.User(id=789))

    db_session.add(messenger.Message(id=1000, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 8, 8, 23, 59, 59),
        text="Old hello"))

    db_session.add(messenger.Message(id=1001, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 9, 8, 23, 59, 59),
        text="¡This is a Unicode message with 256 characters or less in it!"))

    db_session.add(messenger.Message(id=1002, sender_id=123, recipient_id=456,
        datetime=datetime.datetime(2021, 9, 9, 8, 59, 59),
        text="Hello"))

    db_session.add(messenger.Message(id=1003, sender_id=456, recipient_id=123,
        datetime=datetime.datetime(2021, 9, 9, 8, 59, 59),
        text="Hello back"))

    db_session.add(messenger.Message(id=1004, sender_id=123, recipient_id=789,
        datetime=datetime.datetime(2021, 9, 9, 9, 59, 59),
        text="Hello other"))

    db_session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

