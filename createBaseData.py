from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Properties, UserPropertyAssigned, GuideBusyDates 
from database_setup import GuideLocations, GuideLanguage, PrivateChat, Reviews, Country, Cities
from flask import json
import json
from random import randint
import datetime
import random

engine = create_engine('sqlite:///findYourTourGuide.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Cleand DB and start over

# Delete all guideLanguages
guideLanguages = session.query(GuideLanguage).all()
if guideLanguages:
     for lng in guideLanguages:
          session.delete(lng)
     session.commit()

# Delete all suideLocations
guideLocations = session.query(GuideLocations).all()
if guideLocations:
     for loc in guideLocations:
          session.delete(loc)
     session.commit()

# Delete all users guideBusyDates
guideBusyDates = session.query(GuideBusyDates).all()
if guideBusyDates:
     for date in guideBusyDates:
          session.delete(date)
     session.commit()

# Delete all users userPropertyAssigned
userPropertyAssigned = session.query(UserPropertyAssigned).all()
if userPropertyAssigned:
     for userProp in userPropertyAssigned:
          session.delete(userProp)
     session.commit()

# Delete all users properties
"""properties = session.query(Properties).all()
if properties:
     for prop in properties:
          session.delete(prop)
     session.commit()"""

# Delete all users privateChat
privateChat = session.query(PrivateChat).all()
if privateChat:
     for chat in privateChat:
          session.delete(chat)
     session.commit()

# Delete all users reviews
reviews = session.query(Reviews).all()
if reviews:
     for review in reviews:
          session.delete(review)
     session.commit()

# Delete all users users
users = session.query(User).all()
if users:
     for user in users:
          session.delete(user)
     session.commit()

props = session.query(Properties).all()
if props:
     for p in props:
          session.delete(p)
     session.commit()

# Enter new data to the DB

# Create users of type 'traveler'
user1 = User(firstName = "Dina", lastName = "Ferdinskoif", email="dinaferdin@gmail.com", userName="dinaf",
 password="12345",userType="T")
user2 = User(firstName = "Alexander", lastName = "Ferdinskoif", email="alexanderferdin@gmail.com", userName="alexf",
     password="12345",userType="T")
user3 = User(firstName = "Grer", lastName = "Grin", email="greggrin@gmail.com", userName="gregG",
     password="12345",userType="T")
user4 = User(firstName = "Alona", lastName = "Grin", email="alonagrin@gmail.com", userName="AlonaG",
     password="12345",userType="T")
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.commit()

# Fetch travelers ids
userId1 = session.query(User).filter(User.email == "dinaferdin@gmail.com").one()
userId2 = session.query(User).filter(User.email == "alexanderferdin@gmail.com").one()
userId3 = session.query(User).filter(User.email == "greggrin@gmail.com").one()
userId4 = session.query(User).filter(User.email == "alonagrin@gmail.com").one()


# Create users of type 'guide'
guide1 = User(firstName = "Bob", lastName = "Lubovich", email="boblob@gmail.com", userName="bobl",
     password="12345",userType="G")
guide2 = User(firstName = "Chan", lastName = "Yahu mai", email="chanyahu@gmail.com", userName="chany",
     password="12345",userType="G")

guide3 = User(firstName = "John", lastName = "Gold", email="johngold@gmail.com", userName="johng",
     password="12345",userType="G")

guide4 = User(firstName = "Mike", lastName = "Rees", email="mikerees@gmail.com", userName="miker",
     password="12345",userType="G")

session.add(guide1)
session.add(guide2)
session.add(guide3)
session.add(guide4)
session.commit()


# Fetch guides ids
guideId1 = session.query(User).filter(User.email == "boblob@gmail.com").one()
guideId2 = session.query(User).filter(User.email == "chanyahu@gmail.com").one()
guideId3 = session.query(User).filter(User.email == "johngold@gmail.com").one()
guideId4 = session.query(User).filter(User.email == "mikerees@gmail.com").one()

print(guideId1.id)

# Create guideLocations 
"""
guideLocations1 = GuideLocations(userId = guideId1.id, country = "England", city="London")
guideLocations2 = GuideLocations(userId = guideId1.id, country = "England", city="Manchester")
guideLocations3 = GuideLocations(userId = guideId1.id, country = "Skotland", city="Skotland city")
guideLocations4 = GuideLocations(userId = guideId2.id, country = "China", city="Hongkong")
guideLocations5 = GuideLocations(userId = guideId2.id, country = "China", city="Guangzhou")
guideLocations6 = GuideLocations(userId = guideId2.id, country = "China", city="Yansgshou")
guideLocations7 = GuideLocations(userId = guideId2.id, country = "China", city="Zangiagae")
guideLocations8 = GuideLocations(userId = guideId3.id, country = "Israel", city="Jerusalem")
guideLocations9 = GuideLocations(userId = guideId4.id, country = "USA", city="New York")
guideLocations10 = GuideLocations(userId = guideId4.id, country = "USA", city="Navada")


session.add(guideLocations1)
session.add(guideLocations2)
session.add(guideLocations3)
session.add(guideLocations4)
session.add(guideLocations5)
session.add(guideLocations6)
session.add(guideLocations7)
session.add(guideLocations8)
session.add(guideLocations9)
session.add(guideLocations10)

"""

if not session.query(Properties).all():
     prop1 = Properties(propertyName = "description")
     prop2 = Properties(propertyName = "age")
     prop3 = Properties(propertyName = "education")
     prop4 = Properties(propertyName = "certificate")
     prop5 = Properties(propertyName = "gender")
     prop6 = Properties(propertyName = "yearsOfExperience")
     prop7 = Properties(propertyName = "photo")
     session.add(prop1)
     session.add(prop2)
     session.add(prop3)
     session.add(prop4)
     session.add(prop5)
     session.add(prop6)
     session.add(prop7)

session.commit()

photoProp = session.query(Properties).filter(Properties.propertyName == 'photo').one()

newPhotoPropertyAssigned1 = UserPropertyAssigned(
            propertyId = photoProp.id, userId = guideId1.id, propertyValue = 'guide1.jpg')
            
newPhotoPropertyAssigned2 = UserPropertyAssigned(
            propertyId = photoProp.id, userId = guideId2.id, propertyValue = 'guide2.jpg')

newPhotoPropertyAssigned3 = UserPropertyAssigned(
            propertyId = photoProp.id, userId = guideId3.id, propertyValue = 'guide3.jpg')

newPhotoPropertyAssigned4 = UserPropertyAssigned(
            propertyId = photoProp.id, userId = guideId4.id, propertyValue = 'guide4.jpg')

session.add(newPhotoPropertyAssigned1)
session.add(newPhotoPropertyAssigned2)
session.add(newPhotoPropertyAssigned3)
session.add(newPhotoPropertyAssigned4)

session.commit()

user5 = session.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == 5,\
 Properties.propertyName == 'photo', Properties.id == UserPropertyAssigned.propertyId).one()
print(user5.propertyValue)

descriptionProp = session.query(Properties).filter(Properties.propertyName == 'description').one()

newdescriptionPropertyAssigned1 = UserPropertyAssigned(
            propertyId = descriptionProp.id, userId = guideId1.id, 
            propertyValue = 'I love traveling and comunicating with people. Travel is my passion.'
            ' I was born in bla blas and since bla I became bla bla.')
            
newdescriptionPropertyAssigned2 = UserPropertyAssigned(
            propertyId = descriptionProp.id, userId = guideId2.id, propertyValue = 'I love traveling and comunicating with people.'
            ' Travel is my passion.'
            ' I was born in bla blas and since bla I became bla bla.')

newdescriptionPropertyAssigned3 = UserPropertyAssigned(
            propertyId = descriptionProp.id, userId = guideId3.id, propertyValue = 'I love traveling and comunicating with people.'
            ' Travel is my passion.'
            ' I was born in bla blas and since bla I became bla bla.')

newdescriptionPropertyAssigned4 = UserPropertyAssigned(
            propertyId = descriptionProp.id, userId = guideId4.id, propertyValue = 'I love traveling and comunicating with people.'
            ' Travel is my passion.'
            ' I was born in bla blas and since bla I became bla bla.')

session.add(newdescriptionPropertyAssigned1)
session.add(newdescriptionPropertyAssigned2)
session.add(newdescriptionPropertyAssigned3)
session.add(newdescriptionPropertyAssigned4)

session.commit()

certificateProp = session.query(Properties).filter(Properties.propertyName == 'certificate').one()

newcertificatePropertyAssigned1 = UserPropertyAssigned(
            propertyId = certificateProp.id, userId = guideId1.id, 
            propertyValue = 'Technion')
            
newcertificatePropertyAssigned2 = UserPropertyAssigned(
            propertyId = certificateProp.id, userId = guideId2.id, propertyValue = 'Travellers college')

newcertificatePropertyAssigned3 = UserPropertyAssigned(
            propertyId = certificateProp.id, userId = guideId3.id, propertyValue = 'Agencies Inc')

newcertificatePropertyAssigned4 = UserPropertyAssigned(
            propertyId = certificateProp.id, userId = guideId4.id, propertyValue = 'Travel master')

session.add(newcertificatePropertyAssigned1)
session.add(newcertificatePropertyAssigned2)
session.add(newcertificatePropertyAssigned3)
session.add(newcertificatePropertyAssigned4)

session.commit()

ageProp = session.query(Properties).filter(Properties.propertyName == 'age').one()

newagePropPropertyAssigned1 = UserPropertyAssigned(
            propertyId = ageProp.id, userId = guideId1.id, 
            propertyValue = '67')
            
newagePropPropertyAssigned2 = UserPropertyAssigned(
            propertyId = ageProp.id, userId = guideId2.id, propertyValue = '43')

newagePropPropertyAssigned3 = UserPropertyAssigned(
            propertyId = ageProp.id, userId = guideId3.id, propertyValue = '29')

newagePropPropertyAssigned4 = UserPropertyAssigned(
            propertyId = ageProp.id, userId = guideId4.id, propertyValue = '39')

session.add(newagePropPropertyAssigned1)
session.add(newagePropPropertyAssigned2)
session.add(newagePropPropertyAssigned3)
session.add(newagePropPropertyAssigned4)

session.commit()

yearsOfExperienceProp = session.query(Properties).filter(Properties.propertyName == 'yearsOfExperience').one()

newyearsOfExperiencePropPropertyAssigned1 = UserPropertyAssigned(
            propertyId = yearsOfExperienceProp.id, userId = guideId1.id, propertyValue = '3')
            
newyearsOfExperiencePropPropertyAssigned2 = UserPropertyAssigned(
            propertyId = yearsOfExperienceProp.id, userId = guideId2.id, propertyValue = '12')

newyearsOfExperiencePropPropertyAssigned3 = UserPropertyAssigned(
            propertyId = yearsOfExperienceProp.id, userId = guideId3.id, propertyValue = '20')

newyearsOfExperiencePropPropertyAssigned4 = UserPropertyAssigned(
            propertyId = yearsOfExperienceProp.id, userId = guideId4.id, propertyValue = '1')

session.add(newyearsOfExperiencePropPropertyAssigned1)
session.add(newyearsOfExperiencePropPropertyAssigned2)
session.add(newyearsOfExperiencePropPropertyAssigned3)
session.add(newyearsOfExperiencePropPropertyAssigned4)

session.commit()

user5 = session.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == 5,\
 Properties.propertyName == 'yearsOfExperience', Properties.id == UserPropertyAssigned.propertyId).one()
print('this is yearsof %s' %user5.propertyValue)


"""if not session.query(Languages).all():
     lang1 = Languages (language= 'Albanian')   
     session.add(lang1)
     lang2 = Languages (language= 'Arabic')   
     session.add(lang2)
     lang3 = Languages (language= 'Azerbaijani')   
     session.add(lang3)
     lang4 = Languages (language= 'Basque')   
     session.add(lang4)
     lang5 = Languages (language= 'Belorussian')
     session.add(lang5)
     lang6 = Languages (language= 'Bengali')   
     session.add(lang6)
     lang7 = Languages (language= 'Brazilian Portuguese')   
     session.add(lang7)
     lang8 = Languages (language= 'Breton')   
     session.add(lang8)
     lang9 = Languages (language= 'Bulgarian')
     session.add(lang9)
     lang10 = Languages (language= 'Canadian French')   
     session.add(lang10)
     lang11 = Languages (language= 'Catalan')   
     session.add(lang11)
     lang12 = Languages (language= 'Chinese (Mandarin)')   
     session.add(lang12)
     lang13 = Languages (language= 'Croatian')  
     session.add(lang13)
     lang14 = Languages (language= 'Czech')   
     session.add(lang14)
     lang15 = Languages (language= 'Danish')   
     session.add(lang15)
     lang16 = Languages (language= 'Dutch')   
     session.add(lang16)
     lang17 = Languages (language= 'English')   
     session.add(lang17)
     lang18 = Languages (language= 'European Portuguese')   
     session.add(lang18)
     lang19 = Languages (language= 'Esperanto')   
     session.add(lang19)
     lang20 = Languages (language= 'Estonian')   
     session.add(lang20)
     lang21 = Languages (language= 'Farsi')   
     session.add(lang21)
     lang22 = Languages (language= 'Finnish')   
     session.add(lang22)
     lang23 = Languages (language= 'Flemish')   
     session.add(lang23)
     lang24 = Languages (language= 'French')   
     session.add(lang24)
     lang25 = Languages (language= 'Galician')   
     session.add(lang25)
     lang26 = Languages (language= 'German')   
     session.add(lang26)
     lang27 = Languages (language= 'Greek')   
     session.add(lang27)
     lang28 = Languages (language= 'Guarani')   
     session.add(lang28)
     lang29 = Languages (language= 'Haitian Creole')   
     session.add(lang29)
     lang30 = Languages (language= 'Hawaiian')   
     session.add(lang30)
     lang31 = Languages (language= 'Hebrew')   
     session.add(lang31)
     lang32 = Languages (language= 'Hindi')   
     session.add(lang32)
     lang33 = Languages (language= 'Hungarian')   
     session.add(lang33)
     lang34 = Languages (language= 'Icelandic')   
     session.add(lang34)
     lang35 = Languages (language= 'Indonesian')   
     session.add(lang35)
     lang36 = Languages (language= 'Irish')   
     session.add(lang36)
     lang37 = Languages (language= 'Italian')   
     session.add(lang37)
     lang38 = Languages (language= 'Japanese')   
     session.add(lang38)
     lang39 = Languages (language= 'Korean')   
     session.add(lang39)
     lang40 = Languages (language= 'Latin')   
     session.add(lang40)
     lang41 = Languages (language= 'Latvian')   
     session.add(lang41)
     lang42 = Languages (language= 'Lithuanian')   
     session.add(lang42)
     lang43 = Languages (language= 'Luganda')   
     session.add(lang43)
     lang44 = Languages (language= 'Luxembourgish')   
     session.add(lang44)
     lang45 = Languages (language= 'Malagasy')   
     session.add(lang45)
     lang46 = Languages (language= 'Malay')   
     session.add(lang46)
     lang47 = Languages (language= 'Norwegian')   
     session.add(lang47)
     lang48 = Languages (language= 'Pidgin English')   
     session.add(lang48)
     lang49 = Languages (language= 'Polish')   
     session.add(lang49)
     lang50 = Languages (language= 'Quechua')   
     session.add(lang50)
     lang51 = Languages (language= 'Romanian')   
     session.add(lang51)
     lang52 = Languages (language= 'Russian')   
     session.add(lang52)
     lang53 = Languages (language= 'Scottish Gaelic')   
     session.add(lang53)
     lang54 = Languages (language= 'Serbian')   
     session.add(lang54)
     lang55 = Languages (language= 'Slovak')   
     session.add(lang55)
     lang56 = Languages (language= 'Slovene')   
     session.add(lang56)
     lang57 = Languages (language= 'Somali')   
     session.add(lang57)
     lang58 = Languages (language= 'Sotho')   
     session.add(lang58)
     lang59 = Languages (language= 'Spanish')   
     session.add(lang59)
     lang60 = Languages (language= 'Swahili')   
     session.add(lang60)
     lang61 = Languages (language= 'Swedish')   
     session.add(lang61)
     lang62 = Languages (language= 'Tagalog')   
     session.add(lang62)
     lang63 = Languages (language= 'Tahitian')   
     session.add(lang63)
     lang64 = Languages (language= 'Thai')   
     session.add(lang64)
     lang65 = Languages (language= 'Tswana')   
     session.add(lang65)
     lang66 = Languages (language= 'Turkish')   
     session.add(lang66)
     lang67 = Languages (language= 'Ukrainian')   
     session.add(lang67)
     lang68 = Languages (language= 'Urdu')   
     session.add(lang68)
     lang69 = Languages (language= 'Vietnamese')   
     session.add(lang69)
     lang70 = Languages (language= 'Welsh')   
     session.add(lang70)
     lang71 = Languages (language= 'Wolof')   
     session.add(lang71)
     lang72 = Languages (language= 'Xhosa')   
     session.add(lang72)
     lang73 = Languages (language= 'Yiddish')   
     session.add(lang73)
     lang74 = Languages (language= 'Yoruba')   
     session.add(lang74)
     lang75 = Languages (language= 'Zulu')   
     session.add(lang75)
     lang76 = Languages (language= 'Portuguese')   
     session.add(lang76) """

session.commit()

# Create guideLanguages 
guideLanguage1 = GuideLanguage(userId = guideId1.id, languageName = "English")
guideLanguage2 = GuideLanguage(userId = guideId1.id, languageName = "Spanish")
guideLanguage3 = GuideLanguage(userId = guideId2.id, languageName = "Chines")
guideLanguage4 = GuideLanguage(userId = guideId2.id, languageName = "English")
guideLanguage5 = GuideLanguage(userId = guideId2.id, languageName = "French")
guideLanguage6 = GuideLanguage(userId = guideId3.id, languageName = "Hebrew")
guideLanguage7 = GuideLanguage(userId = guideId3.id, languageName = "Protugese")
guideLanguage8 = GuideLanguage(userId = guideId4.id, languageName = "English")

session.add(guideLanguage1)
session.add(guideLanguage2)
session.add(guideLanguage3)
session.add(guideLanguage4)
session.add(guideLanguage5)
session.add(guideLanguage6)
session.add(guideLanguage7)
session.add(guideLanguage8)
session.commit()

countries = session.query(Country).all()
for c in countries:
    session.delete(c)
session.commit() 

c1 = Country(name = "China")
session.add(c1)
c2 = Country(name = "Japan")
session.add(c2)
c3 = Country(name = "Thailand")
session.add(c3)
c4 = Country(name = "India")
session.add(c4)
c5 = Country(name = "Malaysia")
session.add(c5)
c6 = Country(name = "Republic of Korea")
session.add(c6)
c7 = Country(name = "Hong Kong")
session.add(c7)
c8 = Country(name = "Taiwan")
session.add(c8)
c9 = Country(name = "Philippines")
session.add(c9)
c10 = Country(name = "Australia")
session.add(c10)
c11 = Country(name = "Vietnam")
session.add(c11)
c12 = Country(name = "Russia")
session.add(c12)
c13 = Country(name = "France")
session.add(c13)
c14 = Country(name = "Germany")
session.add(c14)
c15 = Country(name = "Israel")
session.add(c15)
c16 = Country(name = "Sweden")
session.add(c16)
c17 = Country(name = "Italy")
session.add(c17)
c18 = Country(name = "Netherlands")
session.add(c18)
c19 = Country(name = "Greece")
session.add(c19)
c20 = Country(name = "Spain")
session.add(c20)
c21 = Country(name = "Austria")
session.add(c21)
c22 = Country(name = "United Kingdom")
session.add(c22)
c23 = Country(name = "Belgium")
session.add(c23)
c24 = Country(name = "Portugal")
session.add(c24)
c25 = Country(name = "Denmark")
session.add(c25)
c26 = Country(name = "Slovenia")
session.add(c26)
c27 = Country(name = "Norway")
session.add(c27)
c28 = Country(name = "Mexico")
session.add(c28)
c29 = Country(name = "Canada")
session.add(c29)
c30 = Country(name = "Ukraine")
session.add(c30)
c31 = Country(name = "Cyprus")
session.add(c31)
c32 = Country(name = "Czech Republic")
session.add(c32)
c33 = Country(name = "Switzerland")
session.add(c33)
c34 = Country(name = "Romania")
session.add(c34)
c35 = Country(name = "Hungary")
session.add(c35)
c36 = Country(name = "Georgia")
session.add(c36)
c37 = Country(name = "Brazil")
session.add(c37)
c38 = Country(name = "Azerbaijan")
session.add(c38)
c39 = Country(name = "Slovakia")
session.add(c39)
c40 = Country(name = "Serbia")
session.add(c40)
c41 = Country(name = "Iceland")
session.add(c41)
c42 = Country(name = "Bulgaria")
session.add(c42)
c43 = Country(name = "Macedonia")
session.add(c43)
c44 = Country(name = "Liechtenstein")
session.add(c44)
c45 = Country(name = "Jersey")
session.add(c45)
c46 = Country(name = "Poland")
session.add(c46)
c47 = Country(name = "Ireland")
session.add(c47)
c48 = Country(name = "Croatia")
session.add(c48)
c50 = Country(name = "Estonia")
session.add(c50)
c51 = Country(name = "Latvia")
session.add(c51)
c52 = Country(name = "Isle of Man")
session.add(c52)
c53 = Country(name = "Luxembourg")
session.add(c53)
c54 = Country(name = "Armenia")
session.add(c54)
c55 = Country(name = "Kenya")
session.add(c55)
c56 = Country(name = "Chile")
session.add(c56)
c57 = Country(name = "Guadeloupe")
session.add(c57)
c58 = Country(name = "Martinique")
session.add(c58)
c59 = Country(name = "French Guiana")
session.add(c59)
c60 = Country(name = "Dominican Republic")
session.add(c60)
c61 = Country(name = "Guam")
session.add(c61)
c62 = Country(name = "Puerto Rico")
session.add(c62)
c63 = Country(name = "Mongolia")
session.add(c63)
c64 = Country(name = "New Zealand")
session.add(c64)
c65 = Country(name = "Singapore")
session.add(c65)
c66 = Country(name = "Indonesia")
session.add(c66)
c67 = Country(name = "Nepal")
session.add(c67)
c68 = Country(name = "Papua New Guinea")
session.add(c68)
c69 = Country(name = "Panama")
session.add(c69)
c70 = Country(name = "Costa Rica")
session.add(c70)
c71 = Country(name = "Peru")
session.add(c71)
c72 = Country(name = "Belize")
session.add(c72)
c73 = Country(name = "Nigeria")
session.add(c73)
c74 = Country(name = "Venezuela")
session.add(c74)
c75 = Country(name = "Bahamas")
session.add(c75)
c76 = Country(name = "Morocco")
session.add(c76)
c77 = Country(name = "Colombia")
session.add(c77)
c78 = Country(name = "Barbados")
session.add(c78)
c79 = Country(name = "Egypt")
session.add(c79)
c80 = Country(name = "Argentina")
session.add(c80)
c81 = Country(name = "Brunei")
session.add(c81)
c82 = Country(name = "Aruba")
session.add(c82)
c83 = Country(name = "Bangladesh")
session.add(c83)
c84 = Country(name = "Cambodia")
session.add(c84)
c85 = Country(name = "Macao")
session.add(c85)
c86 = Country(name = "Maldives")
session.add(c86)
c87 = Country(name = "Montenegro")
session.add(c87)
c88 = Country(name = "Fiji")
session.add(c88)
c89 = Country(name = "Bermuda")
session.add(c89)
c90 = Country(name = "Ecuador")
session.add(c90)
c91 = Country(name = "South Africa")
session.add(c91)
c92 = Country(name = "Malta")
session.add(c92)
c93 = Country(name = "Tanzania")
session.add(c93)
c94 = Country(name = "Zambia")
session.add(c94)
c95 = Country(name = "Madagascar")
session.add(c95)
c96 = Country(name = "Namibia")
session.add(c96)
c97 = Country(name = "Cameroon")
session.add(c97)
c98 = Country(name = "Malawi")
session.add(c98)
c99 = Country(name = "Greenland")
session.add(c99)
c100 = Country(name = "Cayman Islands")
session.add(c100)
c101 = Country(name = "Jamaica")
session.add(c101)
c102 = Country(name = "Monaco")
session.add(c102)
c103 = Country(name = "Paraguay")
session.add(c103)
c104 = Country(name = "Nicaragua")
session.add(c104)
c105 = Country(name = "El Salvador")
session.add(c105)
c106 = Country(name = "Andorra")
session.add(c106)     
c108 = Country(name = "Sri Lanka")
session.add(c108)
c109 = Country(name = "Haiti")
session.add(c109)
c110 = Country(name = "Uruguay")
session.add(c110)
c111 = Country(name = "Cuba")
session.add(c111)
c112 = Country(name = "Ethiopia")
session.add(c112)

session.commit()

countries = session.query(Country).all()



countriesToCities = json.loads(open('countriesToCitiesNew.json', 'r').read())
for c in countries:
    country = session.query(Country).filter(Country.name == c.name).one()
    for city in countriesToCities[c.name]:
        newCity = Cities(countryId = country.id , city = city)
        session.add(newCity)
        session.commit()
    print('finish %s' %c.name)

cities = session.query(Cities).all()
for c in cities:
    print(c.city, c.countryId)


#china = countriesToCities['China']
#print(china['cities'])

# print(countriesToCities)

# CLIENT_ID = json.loads(
  #  open('client_secrets.json', 'r').read())



"""json_data=open(countriesToCities.json).read()

data = json.loads(json_data)
pprint(data)
"""