from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Unicode
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))
    datetime = Column(DateTime())
    text = Column(Unicode(256))

    def to_dict(self):
        return {
            'id': self.id,
            'sender-id': self.sender_id,
            'recipient-id': self.recipient_id,
            'datetime': self.datetime.isoformat(),
            'text': self.text,
        }

