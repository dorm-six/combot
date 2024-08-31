from sqlalchemy import Column, BigInteger, String, DateTime, Float

from app.db.models import Base


class ChatExperience(Base):
    __tablename__ = "chat_xp"

    chat_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    last_user_name = Column(String(length=511), default="")
    experience = Column(BigInteger, default=0)
    last_exp_update = Column(DateTime, nullable=True, default=None)


# TODO Experience log? I'm having some trouble imagining the way it should work.
#  Have multiple tops, monthly/yearly, and use a window to calculate the xp?
#  But what about levels? To me, it doesn't make much sense. Easier to filter
#  by last_exp_update IMO.


class ChatJackpotProbability(Base):
    __tablename__ = "chat_xp_jackpot_probability"

    chat_id = Column(BigInteger, primary_key=True)
    jackpot_prob = Column(Float, nullable=False, default=0)
