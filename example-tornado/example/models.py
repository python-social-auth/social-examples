from sqlalchemy import Column, Integer, String

from app import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
