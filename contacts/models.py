from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Integer, String


Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dateofbirth = Column(Date)

    emails = relationship('Email', back_populates='person')
    phones = relationship('PhoneNumber', back_populates='person')


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer, primary_key=True) # useless, but the ORM needs it

    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', uselist=False, back_populates='emails')
    email = Column(String)


class PhoneNumber(Base):
    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True) # useless, but the ORM needs it

    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', uselist=False, back_populates='phones')
    phone = Column(String)
