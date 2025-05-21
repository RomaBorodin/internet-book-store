from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

from db.models import Base
from config import settings

engine = create_engine(url=settings.DATABASE_URL)
session_local = scoped_session(session_factory=sessionmaker(autocommit=False))


def init_db():
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope():
    session = session_local()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
