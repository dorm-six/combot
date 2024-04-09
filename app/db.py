from __future__ import unicode_literals, absolute_import, print_function

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import DATABASE_URL

# --------------
# --- ENGINE ---
# --------------

if 'sqlite:///:memory:' == DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 10}, echo=True)

# ------- #
# Session #
# ------- #

Session = sessionmaker(bind=engine)

def new_session():
    """ Creates new sqlalchemy session """
    return Session()

# ------------
# --- Base ---
# ------------

Base = declarative_base()

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
    