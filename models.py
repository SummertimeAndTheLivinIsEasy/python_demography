from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.inspection import inspect
# from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///foo.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts")


# trip_photo = Table('trip_photo', Base.metadata,
#     Column('trip_id', Integer(), ForeignKey("trips.id")),
#     Column('photo_id', Integer(), ForeignKey("photos.id"))
# )
#
# class Trip_type(Base):
#     __tablename__ = 'trip_types'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False, unique=True)
#     trip = relationship("Trip", backref='trip_types')

class Trip_level(Base):
    __tablename__ = 'trip_levels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    # trip = relationship("Trip", backref='trip_levels')

    def __repr__(self):
        return f'{self.id}'


# class Trip_description(Base):
#     __tablename__ = 'trip_descriptions'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(100), nullable=False, unique=True)
#     how_to_go = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     track = Column(String, nullable=False)
#     route_length = Column(Integer, nullable=False)
#     official_website_link = Column(String, nullable=False)
#     trip = relationship("Trip", backref='trip_descriptions')
#
# class Trip_photo(Base):
#     __tablename__ = 'trip_photos'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     photo_id = Column(Integer, ForeignKey('photos.id'))
#     trip_id = Column(Integer, ForeignKey('trips.id'))
#
# class Photo(Base):
#     __tablename__ = 'photos'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False, unique=True)
#     trips = relationship("Trip_photo", backref='photos')
#
#
# class Trip(Base):
#     __tablename__ = 'trips'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     trip_type_id = Column(Integer(), ForeignKey('trip_types.id'))
#     trip_type = relationship("Trip_type")
#     trip_level_id = Column(Integer(), ForeignKey('trip_levels.id'))
#     trip_level = relationship("Trip_level", backref='trips')
#     trip_description_id = Column(Integer(), ForeignKey('trip_descriptions.id'))
#     trip_description = relationship("Trip_description")
#     photos = relationship("Trip_photo", backref='trips')
#     comments = relationship("Comment", backref='trips')
#
# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(100), nullable=False, unique=True)
#     about_me = Column(String, nullable=True)
#     email = Column(String(100), index=True,
#                               unique=True, nullable=True)
#     hashed_password = Column(String, nullable=True)
#
# class Comment(Base):
#     __tablename__ = 'comment'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     description = Column(String, nullable=True)
#     trip_id = Column(Integer, ForeignKey('trips.id'))
#     trip = relationship("Trip")
#


Base.metadata.create_all(engine)
