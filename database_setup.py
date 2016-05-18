import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    userName = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    userType = Column(String(1))

    @property
    def serialize(self):
        
        return{
            'id': self.id,
            'firstName' : self.firstName,
            'lastName' : self.lastName,
            'email' : self.email,
            'userName' : self.userName,
            'password' : self.password,
            'userType' : self.userType
            }


class Properties(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    propertyName = Column(String(50), nullable=False)

    @property
    def serialize(self):
        
        return{
            'id': self.id,
            'propertyName' : self.propertyName
            }

class UserPropertyAssigned(Base):
    __tablename__ = 'userPropertyAssigned'

    propertyId = Column(Integer, primary_key=True)
    userId = Column(Integer, primary_key=True)
    propertyValue = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    property_id = Column(Integer, ForeignKey('properties.id'))
    properties = relationship(Properties) 

    @property
    def serialize(self):
    

        return{
            'propertyId': self.propertyId,
            'propertyValue' : self.propertyValue,
            'userId' : self.userId
            }

class GuideBusyDates(Base):
    __tablename__ = 'guideBusyDates'

    userId = Column(Integer, primary_key=True)
    startDate = Column(Date, primary_key=True)
    endDate = Column(Date, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        
        return{
            'userId' : self.userId,
            'startDate' : self.startDate.strftime('%d-%m-%Y'),
            'endDate' : self.endDate.strftime('%d-%m-%Y')
            }

class GuideLocations(Base):
    __tablename__ = 'guideLocations'

    userId = Column(Integer, primary_key=True)
    location = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        
        return{
            'userId' : self.userId,
            'location' : self.location
	    }

class GuideLanguage(Base):
    __tablename__ = 'guideLanguage'

    userId = Column(Integer, primary_key=True)
    languageName = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        
        return{
            'userId' : self.userId,
            'languageName' : self.languageName
            }

class PrivateChat(Base):
    __tablename__ = 'privateChat'

    id = Column(Integer, primary_key=True)
    userIdWriter = Column(Integer, nullable=False)
    userIdReceiver = Column(Integer, nullable=False)
    headline = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestmp = Column(DateTime(timezone=True), default=func.now())
    user_id_writer = Column(Integer, ForeignKey('user.id'))
    user_writer = relationship("User", foreign_keys=[user_id_writer])
    user_id_receiver = Column(Integer, ForeignKey('user.id'))
    user_receiver = relationship("User", foreign_keys=[user_id_receiver])


    @property
    def serialize(self):
        
        return{
            'id' : self.id,
            'userIdWriter' : self.userIdWriter,
            'userIdReceiver' : self.userIdReceiver,
            'headline' : self.headline,
            'content' : self.content,
            'timestmp' : self.timestmp.strftime('%d/%m/%Y %H:%M:%S')
            }

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    userIdWriter = Column(Integer, nullable=False)
    userIdReceiver = Column(Integer, nullable=False)
    headline = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestmp = Column(DateTime(timezone=True), default=func.now())
    grade = Column(Integer, nullable=False)
    user_id_writer = Column(Integer, ForeignKey('user.id'))
    user_writer = relationship("User", foreign_keys=[user_id_writer])
    user_id_receiver = Column(Integer, ForeignKey('user.id'))
    user_receiver = relationship("User", foreign_keys=[user_id_receiver])

    @property
    def serialize(self):
        
        return{
            'id' : self.id,
            'userIdWriter' : self.userIdWriter,
            'userIdReceiver' : self.userIdReceiver,
            'headline' : self.headline,
            'content' : self.content,
            'timestmp' : self.timestmp.strftime('%d/%m/%Y %H:%M:%S'),
            'grade' : self.grade
            }


engine = create_engine('postgresql://tourguide:tourGuideLinuxDina@localhost/findYourTourGuide')

Base.metadata.create_all(engine)
