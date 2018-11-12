from __future__ import unicode_literals, absolute_import, print_function

import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db import Base


class CombotMall(Base):
    __tablename__ = 'combot_mall'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    seller_username = Column(String, nullable=False)
    description = Column(String, nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now)

def get_all_entries():
    session = new_session()
    entries = session.query(CombotMall).all()
    session.close()
    for entry in entries:
        print('{}:@{}:{}:{}'.format(entry.id, entry.seller_username, 
                                    entry.description, entry.create_time))

def delete_by_id(id):
    session = new_session()
    session.query(CombotMall).filter(CombotMall.id == id).delete()
    session.commit()
    session.close()
