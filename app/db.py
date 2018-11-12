from __future__ import unicode_literals, absolute_import, print_function

import datetime

from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import DATABASE_URL

if 'sqlite:///:memory:' == DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL, connect_args={'sslmode':'require'}, echo=True)

# ------- #
# Session #
# ------- #

Session = sessionmaker(bind=engine)

def new_session():
    """ Creates new sqlalchemy session """
    return Session()

# --------------
# --- Tables ---
# --------------

Base = declarative_base()

# class CombotMall(Base):
#     __tablename__ = 'combot_mall'

#     id = Column(Integer, primary_key=True)
#     seller_id = Column(Integer, nullable=False)
#     seller_username = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     create_time = Column(DateTime, nullable=False, default=datetime.datetime.now)

# def get_all_entries():
#     session = new_session()
#     entries = session.query(CombotMall).all()
#     session.close()
#     for entry in entries:
#         print('{}:@{}:{}:{}'.format(entry.id, entry.seller_username, 
#                                     entry.description, entry.create_time))

# def delete_by_id(id):
#     session = new_session()
#     session.query(CombotMall).filter(CombotMall.id == id).delete()
#     session.commit()
#     session.close()

# -------------
# --- Utils ---
# -------------

def init_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)

def refresh_tables():
    drop_tables()
    init_tables()
    