from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Date, Boolean
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


Base.metadata.create_all(bind=engine)
