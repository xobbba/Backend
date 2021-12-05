from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date, Boolean, select
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DB_URI = 'sqlite:///DB.db'
engine = create_engine(SQLALCHEMY_DB_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    date_birth = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    employer = Column(Boolean, default=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    skills = Column(String)
    hobby = Column(String)

    def __repr__(self):
        return f'{"Работодатель" if self.employer else "Работник"}, {self.id}, {self.full_name}, ' \
               f'{self.sex}, {self.date_birth}, {self.age}, {self.login}'


class LikeUsersList(Base):
    __tablename__ = 'LikeUsersList'

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    id_employer = Column(Integer, ForeignKey('user.id'))
    id_user = Column(Integer, ForeignKey('user.id'))
    like = Column(Boolean)

    def __repr__(self):
        return f'{self.id_employer}, {self.id_user}, {self.like}'


Base.metadata.create_all(bind=engine)
