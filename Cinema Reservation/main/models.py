from sqlalchemy import (Column, Integer, String, Boolean,
                        Float, ForeignKey, DateTime,
                        CheckConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from email.utils import parseaddr
from re import compile, match

Base = declarative_base()


class Tutorial(Base):
    __tablename__ = 'tutorial'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, unique=True)
    content = Column(Integer, unique=True)


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


# class Movie(Base):
#     __tablename__ = 'movie'
#     __table_args__ = (
#         CheckConstraint('rating between 0 and 10'),
#     )
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)
#     rating = Column(Float)


# class Projection(Base):
#     __tablename__ = 'projection'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey(Movie.id))
#     movie = relationship(Movie, backref='projections')
#     type = Column(String(3))
#     date = Column(Date)
#     time = Column(Time)


# class Reservation(Base):
#     __tablename__ = 'reservation'
#     __table_args__ = (
#         CheckConstraint('row between 1 and 10'),
#         CheckConstraint('col between 1 and 10'),
#     )
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey(User.id))
#     user = relationship(User, backref='reservations')
#     projection_id = Column(Integer, ForeignKey(Projection.id))
#     projection = relationship(Projection, backref='reservations')
#     row = Column(Integer)
#     col = Column(Integer)
