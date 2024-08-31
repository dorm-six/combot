from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Text,
    Integer,
    String,
    UniqueConstraint,
)

from ..db.models import Base


class CommandInfo(Base):
    __tablename__ = "command_info"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    from_id = Column(BigInteger)
    command_msg_id = Column(BigInteger)
    response_msg_id = Column(BigInteger)
    answered = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("chat_id", "command_msg_id"),
        UniqueConstraint("chat_id", "response_msg_id"),
    )


class ChatInfo(Base):
    __tablename__ = "chat_info"

    id = Column(BigInteger, primary_key=True)
    # TODO channel_id = Column(BigInteger, default=None)


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)


class PinnedMsg(Base):
    __tablename__ = "pinned_msg"

    chat_id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger, primary_key=True)
    pin_id = Column(String, nullable=True)
    pinned = Column(Boolean, default=True)
    # TODO forwarded_to_channel = Column(Boolean, default=False)


class MediaGroup(Base):
    __tablename__ = "media_groups"

    chat_id = Column(BigInteger, primary_key=True)
    msg_id = Column(BigInteger, primary_key=True)
    media_group_id = Column(String(length=255))
    media_type = Column(String(length=255), default=None)
    media_id = Column(String(length=1024), default=None)
    caption = Column(Text, default=None)
