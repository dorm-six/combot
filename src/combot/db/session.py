from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import DATABASE_URL
from .models import Base


def init_db():
    e = create_engine(DATABASE_URL, pool_size=10)
    s = sessionmaker(bind=e)
    return e, s


engine, Session = init_db()


def init_metadata():
    Base.metadata.create_all(engine)


def dbsession(*args, session=Session):
    def uses_db_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            session_created = False
            if "session" in kwargs:
                s = kwargs["session"]
                del kwargs["session"]
            else:
                session_created = True
                s = session()
            result = None
            try:
                result = func(*args, **kwargs, session=s)
            finally:
                if session_created:
                    s.close()
            return result

        return func_wrapper

    if args:
        return uses_db_decorator(args[0])
    return uses_db_decorator
