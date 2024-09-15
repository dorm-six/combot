from sqlalchemy import Column, BigInteger

from ...db.models import Base


class ChatFeed(Base):
    __tablename__ = "feed_forward_chat_feed"

    chat_id = Column(BigInteger, primary_key=True, index=True)
    feed_channel_id = Column(BigInteger, primary_key=True)


class ForwardedMessage(Base):
    __tablename__ = "feed_forward_message_forwarded"

    chat_id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger, primary_key=True)
