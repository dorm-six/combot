from sqlalchemy import Column, BigInteger

from app.db.models import Base


class ChatFeed(Base):
    __tablename__ = "chat_feed"

    chat_id = Column(BigInteger, primary_key=True, index=True)
    feed_channel_id = Column(BigInteger, primary_key=True)


class ForwardedMessage(Base):
    __tablename__ = "chat_feed_forwarded"

    chat_id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger, primary_key=True)
