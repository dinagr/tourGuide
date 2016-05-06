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
#    UserPropertyAssigned = relationship("userPropertyAssigned", cascade="all,delete")
#    GuideBusyDates = relationship("guideBusyDates", cascade="all,delete")
#    GuideLanguage = relationship("guideLanguage", cascade="all,delete")
#    UserPropertyAssigned = relationship("userPropertyAssigned", cascade="all,delete")
#    PrivateChat = relationship("privateChat", cascade="all,delete")
#    Reviews = relationship("reviews", cascade="all,delete")

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

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


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
    propertyValue = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)# , backref=backref("items", cascade="all, delete-orphan"))
    property_id = Column(Integer, ForeignKey('properties.id'))
    properties = relationship(Properties) 
        # ,backref=backref("userPropertyAssigned", cascade="all, delete-orphan"))

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
    country = Column(String, primary_key=True)
    city = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        
        return{
            'userId' : self.userId,
            'country' : self.country,
            'city' : self.city
            }

class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


    @property
    def serialize(self):
        
        return{
            'id' : self.id,
            'name' : self.name
            }


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    countryId = Column(Integer, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)


    @property
    def serialize(self):
        
        return{
            'countryId' : self.countryId,
            'city' : self.city
            }

# class Languages(Base):
    """    __tablename__ = 'languages'

    language = Column(String, primary_key=True)


    @property
    def serialize(self):
        
        return{
            'language' : self.language
            }"""

class GuideLanguage(Base):
    __tablename__ = 'guideLanguage'

    userId = Column(Integer, primary_key=True)
    languageName = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
#    language_id = Column(String, ForeignKey('Languages.language'))
#    language = relationship(Languages)

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
