
Testing is currently by hand. See note at bottom of README.md for how I would do automated testing.

After clearing the db (e.g. `rm /tmp/test.db && python setup_test_db.py`) and running the app, I get the following results using Postman.


## Limit tests

`http://127.0.0.1:5000/messages.json?count-limit=100` returns 

```
{
    "count": 5,
    "messages": [
        {
            "id": 1004,
            "sender-id": 123,
            "recipient-id": 789,
            "datetime": "2021-09-09T09:59:59",
            "text": "Hello other"
        },
        {
            "id": 1002,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello"
        },
        {
            "id": 1003,
            "sender-id": 456,
            "recipient-id": 123,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello back"
        },
        {
            "id": 1001,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-08T23:59:59",
            "text": "¡This is a Unicode message with 256 characters or less in it!"
        },
        {
            "id": 1000,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-08-08T23:59:59",
            "text": "Old hello"
        }
    ]
}
```

This is an expected result, as compared to the records in setup_test_db.py. Results are ordered newest to oldest.


`http://127.0.0.1:5000/messages.json?count-limit=1` returns only the one most recent message.


`http://127.0.0.1:5000/messages.json?day-limit=30` returns 4 records, omitting the oldest.
{
    "count": 4,
    "messages": [
        {
            "id": 1004,
            "sender-id": 123,
            "recipient-id": 789,
            "datetime": "2021-09-09T09:59:59",
            "text": "Hello other"
        },
        {
            "id": 1002,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello"
        },
        {
            "id": 1003,
            "sender-id": 456,
            "recipient-id": 123,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello back"
        },
        {
            "id": 1001,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-08T23:59:59",
            "text": "¡This is a Unicode message with 256 characters or less in it!"
        }
    ]
}

## Sender + recipient + limit tests

`http://127.0.0.1:5000/messages.json?count-limit=100&recipient-id=456&sender-id=123` returns 3 records:

```
{
    "count": 3,
    "messages": [
        {
            "id": 1002,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello"
        },
        {
            "id": 1001,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-08T23:59:59",
            "text": "¡This is a Unicode message with 256 characters or less in it!"
        },
        {
            "id": 1000,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-08-08T23:59:59",
            "text": "Old hello"
        }
    ]
}
```

`http://127.0.0.1:5000/messages.json?day-limit=30&recipient-id=456&sender-id=123` returns 2 records:

```
{
    "count": 2,
    "messages": [
        {
            "id": 1002,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-09T08:59:59",
            "text": "Hello"
        },
        {
            "id": 1001,
            "sender-id": 123,
            "recipient-id": 456,
            "datetime": "2021-09-08T23:59:59",
            "text": "¡This is a Unicode message with 256 characters or less in it!"
        }
    ]
}
```
