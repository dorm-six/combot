from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Text,
    Integer,
    String,
    UniqueConstraint,
    Index,
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
    handle = Column(String, nullable=True)


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}".strip()


class PinnedMsg(Base):
    __tablename__ = "pinned_msg"

    chat_id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger, primary_key=True)
    pin_id = Column(String, nullable=True, index=True)
    pinned = Column(Boolean, default=True)

    __table_args__ = (Index("chat_id", "pin_id", "pinned"),)


class MediaGroupMessage(Base):
    __tablename__ = "media_group_message"

    chat_id = Column(BigInteger, primary_key=True)
    media_group_id = Column(String(length=255), primary_key=True)
    msg_id = Column(BigInteger, primary_key=True)
    caption = Column(Text)
    finalized = Column(Boolean, default=False)

    __table_args__ = (Index("chat_id", "media_group_id", "finalized"),)
