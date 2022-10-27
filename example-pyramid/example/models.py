from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register


DBSession = scoped_session(sessionmaker(expire_on_commit=False))
register(DBSession)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password = Column(String(200), default='')
    name = Column(String(100))
    active = Column(Boolean, default=True)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True
