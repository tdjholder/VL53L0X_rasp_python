from simple_settings import settings


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


engine = create_engine(settings.DB_URL, echo=True)


def get_session():
    """Get a session to create transactions."""
    return sessionmaker(bind=engine)()






