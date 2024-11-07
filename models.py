from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.inspection import inspect
# from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from demography import login_manager

# import demography

engine = create_engine("sqlite:///foo.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts")


class Trip_duration(Base):
    __tablename__ = 'trip_durations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    duration = Column(Integer, nullable=False, unique=True)
    trip = relationship("Trip", backref='trip_durations')


class Trip_type(Base):
    __tablename__ = 'trip_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(100), nullable=False, unique=True)
    # # error https://sqlalche.me/e/20/gkpj
    # id = Column(String(30), primary_key=True, nullable=False, unique=True)
    trip = relationship("Trip", backref='trip_types')


class Trip_level(Base):
    __tablename__ = 'trip_levels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(100), nullable=False, unique=True)
    level_name = Column(String(100), nullable=False, unique=True)
    trip = relationship("Trip", backref='trip_levels')

    def __repr__(self):
        return f'{self.id}'


class Trip_description(Base):
    __tablename__ = 'trip_descriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False, unique=True)
    how_to_go = Column(String, nullable=False)
    description = Column(String, nullable=False)
    track = Column(String, nullable=False)
    route_length = Column(Integer, nullable=False)
    official_website_link = Column(String, nullable=False)
    trip = relationship("Trip", backref='trip_descriptions')
    main_photo_id = Column(Integer(), ForeignKey('photos.id'))


# trip_photo = Table('trip_photo', Base.metadata,
#     Column('trip_id', Integer(), ForeignKey("trips.id")),
#     Column('photo_id', Integer(), ForeignKey("photos.id"))
# )

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(100), nullable=False, unique=True)
    photo_name = Column(String(100), nullable=False)
    trips = relationship("Trip", secondary='trip_photos', back_populates='photos')
    trip_description_id = relationship('Trip_description', backref='photos', uselist=False)


class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_type_id = Column(Integer(), ForeignKey('trip_types.id'))
    trip_duration_id = Column(Integer(), ForeignKey('trip_durations.id'))
    # # error https://sqlalche.me/e/20/gkpj
    # trip_type_id = Column(String(30), ForeignKey('trip_types.id'))
    # trip_type = relationship("Trip_type", backref='trips')
    trip_level_id = Column(Integer(), ForeignKey('trip_levels.id'))
    # trip_level = relationship("Trip_level", backref='trips')
    trip_description_id = Column(Integer(), ForeignKey('trip_descriptions.id'))
    # trip_description = relationship("Trip_description", backref='trips')
    photos = relationship("Photo", secondary='trip_photos', back_populates='trips')
    comments = relationship("Comment", backref='trips')


class Trip_photo(Base):
    __tablename__ = 'trip_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    photo_id = Column(Integer, ForeignKey('photos.id'))

# @login_manager.user_loader
# def load_user(user_id):
#     with Session() as session:
#         return session.get(User, int(user_id))


    # return db.session.query(User).get(user_id)


# class User(UserMixin, Base):
class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    about_me = Column(String, nullable=True)
    email = Column(String(100), index=True,
                   unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    comment = relationship("Comment", backref="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # def get_id(self):
    #     return str(self.id)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    # trip = relationship("Trip", backref='comments')
    user_id = Column(Integer(), ForeignKey('user.id'))


#
# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         with Session() as session:
#             session.commit()
#         return session.query(User).get(user_id)
#     except:
#         return None

# @login_manager.user_loader
# def load_user(id):
#     with Session() as session:
#         session.commit()
#     return session.get(User, int(id))
#
# Base.metadata.create_all(engine)

# parent = Parent(name='John Doe', uuid=str(uuid.uuid4()))
# session.add(parent)
# session.commit()
#
# child = Child(name='Jimmy Doe', uuid=str(uuid.uuid4()))
# session.add(child)
# session.commit()
#
# parent.children.append(child)
#
# print('# Parents')
# for parent in session.query(Parent).all():
#     children = [x.name for x in parent.children]
#     print(f'Parent: name={parent.name}, children={children}')
# print()
#
# print('# Children')
# for child in session.query(Child).all():
#     parents = [x.name for x in child.parents]
#     print(f'Child: name={child.name}, parents={parents}')
# print()
