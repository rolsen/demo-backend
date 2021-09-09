## Database Schema

Users Table
id: primary key integer
# Not implemented: name: char
# Not implemented: password

Contacts Table (Not implemented)

Message Table
id: primary key integer
sender_id: integer
recipient_id: integer
datetime: DATETIME index
    # Stored in UTC
text: unicode max length 256
    # unicode seems best because this app is worldwide, and therefore likely multi-language.



### A note on sharding

Because this is a worldwide app, it could end up requiring database sharding given enough scale. Shards of the Message table could be made according to a location of where the recipient is located. That would be nice for the sake of geographically locating messages close to where they'll likely be accessed most, which allows for better caching and lower latency. (It seems like a safe assumption the recipient will read their messages multiple times and that the recipient is usually located in the same geographical region.) This sharding would not be effective when the recipient is not specified in the GET request.



## AJAX endpoints

GET /users.json
    Not implemented, but this would return user names given ids and vice versa.

GET/POST/PUT/DELETE /contacts.json
    Not implemented, but this would get or alter the contacts of a particular user.

POST /messages.json
    enctype=text/plain, as json
        {
            "sender-id": 123,
            "receiver-id": 456,
            "text": "This is a Unicode message with 256 characters or less in it.",
            "datetime": "2021-09-08 23:59:59"
        }

GET /messages.json?recipient=456&sender=123&count-limit=100
GET /messages.json?recipient=456&sender=123&day-limit=30
GET /messages.json?count-limit=100
GET /messages.json?day-limit=30
    Example return data:
        {
            "count": 100,
            "messages": [
                1000: {
                    "sender-id": 123,
                    "receiver-id": 456,
                    "text": "This is a Unicode message with 256 characters or less in it.",
                    "datetime": "2021-09-08 23:59:59"
                },
                ...
            ],
        }

    To [bypass the cache](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest#bypassing_the_cache), a timestamp may be added to the URL.


## Pagination (not implemented)

Getting all messages from the last 30 days is likely to be too many records to reasonably display at once (and even 100 messages is too much to fit on a mobile screen). Pagination is the solution. I would probably want to do this such that new messages didn't mess up the order of later pages. If there's 20 messages on page 1, ending in message ids 102, 101, and 100 as the oldest, then loading page 1 should start with 99, 98, etc. We can't exactly paginate based on the message count only because then a new message would cause message 100 to show up on page 2. Instead, we would pass message id 100 as the last message we saw, and page 2 would consist of a count of 20 (or less) messages after message 100.

