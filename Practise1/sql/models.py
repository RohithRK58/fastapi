from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__= 'testuser'
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, index=True)
    age = Column(Integer)
    country = Column(String, index=True)

class Loginfo(Base):
    __tablename__ = 'loginfo'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    email = Column(String, index=True)
    