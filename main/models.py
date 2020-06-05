from sqlalchemy import (Column, Integer, String, Boolean,
                        Float, ForeignKey, DateTime,)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tutorial(Base):
    __tablename__ = 'tutorial'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, unique=True)
    content = Column(Integer, unique=True)

    @property
    def words(self):
        return len(self.content.split(' '))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)
    superuser = Column(Boolean)
    next_tutorial_order_id = Column(Integer, ForeignKey(Tutorial.order_id), default=1)
    tutorial = relationship(Tutorial, backref='users')

    def __str__(self):
        return f'{self.id} | {self.username} | {self.email} | {self.password}'


class Text(Base):
    __tablename__ = 'text'
    id = Column(Integer, primary_key=True)
    content = Column(String, unique=True)

    @property
    def words(self):
        return len(self.content.split(' '))


class SpeedTest(Base):
    __tablename__ = 'speedtest'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User, backref='speedtests')
    text_id = Column(Integer, ForeignKey(Text.id))
    text = relationship(Text, backref='speedtests')
    words_per_minute = Column(Float)
    when = Column(DateTime)
