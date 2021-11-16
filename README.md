# Demo Backend API - Rory Olsen


## Dependencies

This app primarily uses Flask and Flask-SQLAlchemy with a sqlite database at `/tmp/test.db`. You can install everything that's needed using a virtual environment like pyenv, then running:

```
pip install -r requirements.txt
```

## Database Setup

To get started, set up the test database:

```
python setup_test_db.py
```

Make sure the current process has write permissions on `/tmp/test.db`, or set a different path (see messenger.py).

## Run the App

First, set the following environment variables:

```
export FLASK_APP=messenger
export FLASK_ENV=development
```

Then run the app:

```
python messenger.py
```

Or, together:

```
(export FLASK_APP=messenger && export FLASK_ENV=development && python messenger.py)
```

## Database Schema

```
Users
    id: primary key integer

Message
    id: primary key integer
    sender_id: integer
    recipient_id: integer
    datetime: DATETIME
     - Stored in UTC
     - Likely candidate for index
    text: unicode max length 256
     - Unicode seems best because this app is worldwide, and therefore likely multi-language.
```


## AJAX endpoints

Hello web team!

Currently the only things that are implemented are getting and posting messages. All endpoints use JSON, so it's expected to use AJAX.

Note that the message `datetime` is UTC and the message `text` is in Unicode. See examples below.

### Post messages

`POST /messages.json`
Uses enctype=text/json for the parameters/data:

```
{
    "sender-id": 123,
    "recipient-id": 456,
    "text": "¡This is a Unicode message with 256 characters or less in it!",
    "datetime": "2021-09-08 23:59:59"
}
```

This returns the new message, including the newly-created id:

```
{
    "id": 3,
    "sender-id": 123,
    "recipient-id": 456,
    "datetime": "2021-09-08T23:59:59",
    "text": "¡This is a Unicode message with 256 characters or less in it!"
}
```

### Get messages

There's a couple of ways to get a list of messages.

Get the most recent messages for given sender and recipient ids, limited by either count or by number of days:

`GET /messages.json?recipient-id=456&sender-id=123&count-limit=100`

`GET /messages.json?recipient-id=456&sender-id=123&day-limit=30`

Get the most recent messages, limited by either count or by number of days:

`GET /messages.json?count-limit=100`

`GET /messages.json?day-limit=30`

Example return data:

```
{
    "count": 100,
    "messages": [
        1000: {
            "id": 1001,
            "sender-id": 123,
            "recipient-id": 456,
            "text": "¡This is a Unicode message with 256 characters or less in it!",
            "datetime": "2021-09-08 23:59:59"
        },
        ...99 more messages, because the "count" is 100
    ],
}
```


### Bypassing the cache

To [bypass the cache](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest#bypassing_the_cache) when getting messages, a timestamp may be added to the URL.


## Testing

I didn't get around to breaking up the application properly into a `controllers/messages.py` and a `models/` dir for the models.

To test the POST route, I would use [pymox](https://pymox.readthedocs.io/en/latest/) to add testing by injecting a fake db session, then make sure the correct model was added via a `session.add(...)` and that `session.commit()` was called.

Further, adding a layer of indirection between the routes and the return values would allow testing. I added a `post_message()` helper function like this.

See TESTING.md for some example tests. (I would convert them into automated tests if I had time.)


