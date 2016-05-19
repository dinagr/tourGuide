from flask import Flask, render_template, request, redirect, send_from_directory
from flask import url_for, flash, jsonify, make_response
from sqlalchemy import create_engine, func
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import exists
from database_setup import *
from flask import session as login_session
import string
import requests
import json 
from werkzeug import secure_filename
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

engine = create_engine('postgresql://tourguide:tourGuideLinuxDina@localhost/findYourTourGuide', convert_unicode=True, pool_size=20, max_overflow=100)
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine, autoflush=False))
app = Flask(__name__)
app.db = session

import createBaseData

# Define where guide photos will be saved and which type of fyles are allowed
full_path_to_upload_folder = os.path.join('/var/www/tourGuide/tourGuide/','static/uploads')
UPLOAD_FOLDER = full_path_to_upload_folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
userPhotos =[]

"""users = app.db.query(User).all()
for u in users:
	app.db.delete(u)
	app.db.commit()
props = app.db.query(UserPropertyAssigned).all()
for p in props:
	app.db.delete(p)
	app.db.commit()
langs = app.db.query(GuideLocations).all()
for l in langs:
	app.db.delete(l)
	app.db.commit()
locs = app.db.query(GuideLanguage).all()
for l in locs:
	app.db.delete(l)
	app.db.commit()"""

"""users = app.db.query(User).all()
for u in users:
	print(u.id, u.userName, u.firstName, u.lastName, u.email, u.userType)
	props = app.db.query(Properties.propertyName ,UserPropertyAssigned.propertyValue).\
	filter(UserPropertyAssigned.userId == u.id, Properties.id == UserPropertyAssigned.propertyId).all()
	for p in props:
		print(p)"""
	

# Check if fily is from allowed type or with allowed file name
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# send email with html content
def send_html_email(recipient, html, subject):
  me = 'findyourtourguide@gmail.com'
  you = recipient
  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = me
  msg['To'] = you
  # Record the MIME types of both parts - text/plain and text/html.
  part2 = MIMEText(html, 'html')
  # Attach parts into message container.
  # According to RFC 2046, the last part of a multipart message, in this case
  # the HTML message, is best and preferred.
  msg.attach(part2)
  try:
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('findyourtourguide', 'Begining04')
    mail.sendmail(me, you, msg.as_string())
    mail.close()
    return True
  except:
    return False

# Check if user allready exist
def isNewUser(username, email):
  if app.db.query(User).filter(User.userName == username).all():
    session.remove()
    return "There is allready a user with the user name %s, Please choose another user name!" %username
  if app.db.query(User).filter(User.email == email).all():
    session.remove()
    return "There is allready a user with the email %s!" %email

# Send a welcome email to new users of type traveller
def sendWelcomeTravelerEmail(email, firstName):
  subject = 'Welcome to \'Find Your Tour Guide\''
  html = ("""
  <html style="font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif">
  <head></head>
    <body>
      <p style="font-size:18px; font-weight: bold;">
        Hello %s
      </p> 
      <p style="font-size:14px;">
        Welcome to  
        <a href="http://ec2-52-36-140-206.us-west-2.compute.amazonaws.com/#/" style="font-weight: bold;">
          FindYourTourGuide
        </a>
      </p>
      <p style="font-size:14px;">
        Start searching the best guide for you and your trip!
      </p>
      <p style="font-size:14px;">
        Sincerely,
      </p>
      <p style="font-size:14px;">
        The 
        <span style="font-weight: bold;">
          FindYourTourGuide
        </span>
        Team.
      </p>
    </body>
  </html>
  """ %firstName)
  send_html_email(email,html, subject)

# Send welcome email to new users of type guide
def sendWelcomeGuideEmail(email, firstName):
  subject = 'Welcome to \'Find Your Tour Guide\''
  html = ("""
  <html style="font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif">
  <head></head>
    <body>
      <p style="font-size:18px; font-weight: bold;">
        Hello %s
      </p> 
      <p style="font-size:14px;">
        Welcome to  
        <a href="http://ec2-52-36-140-206.us-west-2.compute.amazonaws.com/#/" style="font-weight: bold;">
          FindYourTourGuide
        </a>
      </p>
      <p style="font-size:14px;">
        We are excited that you have joined our guides team!
      </p>
      <p style="font-size:14px;">
        Sincerely,
      </p>
      <p style="font-size:14px;">
        The 
        <span style="font-weight: bold;">
          FindYourTourGuide
        </span>
        Team.
      </p>
    </body>
  </html>
  """ %firstName)
  send_html_email(email,html, subject)

# Get the id of property description
def getPropDescription():
  descriptionProp = app.db.query(Properties).filter(Properties.propertyName == 'description').one()
  session.remove()
  return descriptionProp.id

# Get the id of property age
def getPropAge():
  ageProp = app.db.query(Properties).filter(Properties.propertyName == 'age').one()
  session.remove()
  return ageProp.id

# Get the id of property years of experience
def getPropyearsOfExperience():
  yearsOfExperienceProp = app.db.query(Properties).filter(Properties.propertyName == 'yearsOfExperience').one()
  session.remove()
  return yearsOfExperienceProp.id

# Get the id of property certificate
def getPropcertificate():
  certificateProp = app.db.query(Properties).filter(Properties.propertyName == 'certificate').one()
  session.remove()
  return certificateProp.id

# Get the id of property photo
def getPropPhoto():
  photoProp = app.db.query(Properties).filter(Properties.propertyName == 'photo').one()
  session.remove()
  return photoProp.id

# The app functionality
# The main page of the app
# Presents the main search page
@app.route('/')
@app.route('/main/')
def home():
    return render_template('home.html')

# Add new user of type traveller
@app.route('/newUser', methods=['POST'])
def newUser():
  json_data = request.json
  status = ''
  status = isNewUser(json_data['userName'], json_data['email'])
  if not status:
    try:
      newUser = User(
          firstName=json_data['firstName'], lastName = json_data['lastName'],
          email = json_data['email'], userName = json_data['userName']
          ,password = json_data['password'], userType = 'T')
      app.db.add(newUser)
      app.db.commit() 
      session.remove()
      status = 'success'
      sendWelcomeTravelerEmail(json_data['email'], json_data['firstName'])
    except:
      status = 'An error encountered while creating the user, please try again later'
  return jsonify({'result': status})

# Add new user of type guide
@app.route('/newGuide', methods=['POST'])
def newGuide():
  json_data = request.json
  status = ''
  status = isNewUser(json_data['userName'], json_data['email'])
  if not status:
    try:
      newUser = User(
          firstName=json_data['firstName'], lastName = json_data['lastName'],
          email = json_data['email'],userName = json_data['userName']
          ,password = json_data['password'], userType = 'G')
      app.db.add(newUser)
      app.db.commit() 
      status = 'success'
      sendWelcomeGuideEmail(json_data['email'], json_data['firstName'])
      user = app.db.query(User).filter(User.email == json_data['email']).one()
      session.remove()
      return jsonify({'result': status, 'userId': user.id})    
    except:
      status = 'An error encountered while creating the user, please try again later'
  return jsonify({'result': status})

# Check username and password, if correct - loggin user
@app.route('/loginUser', methods=['POST'])
def loginUser():
  json_data = request.json
  try:
    if app.db.query(User).\
      filter(User.userName == json_data['userName'], User.password == json_data['password']).scalar():
      status = 'success'
      user = app.db.query(User).filter(User.userName == json_data['userName']).one()
      login_session['username'] = json_data['userName']
      login_session['user_id'] = user.id
      session.remove()
      return jsonify({'userName': login_session['username'], 
        'userId': login_session['user_id'], 'result': status})  
    else:
      if not app.db.query(User).filter(User.userName == json_data['userName']).scalar(): 
	session.remove()
        return jsonify({'result': 'There is no user with this user name!'})
      else:
        session.remove()
	return jsonify({'result': 'There user name and the pasword don\'t match!'})
  except:
    session.remove()
    status = 'An error encountered while creating the user, please try again later'
    return jsonify({'result': status})

# Logout current user
@app.route('/logout', methods=['GET'])
def logout():
    if login_session:
        login_session['username'] = ''
        login_session['user_id'] = ''
        login_session.clear()
        status = "You have been logged out successfully!"
    else:
        status = 'You were not logged in to begin with!'
    return jsonify({'result': status})

# Send an email to a user with his credentails - the user forgor his username or password
@app.route('/getMyCredentials', methods=['POST'])
def getMyCredentials():
  json_data = request.json
  status = ''
  try:
    if app.db.query(User).filter(User.email == json_data['email']).scalar():
      user = app.db.query(User).filter(User.email == json_data['email']).one()
      subject = 'Your user name and password'
      html = ("""
      <html style="font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif">
        <head></head>
        <body>
          <p style="font-size:18px; font-weight: bold;">
            Hello %s
          </p> 
          <p style="font-size:14px;">
            These are your credentials to 
            <a href="http://ec2-52-36-140-206.us-west-2.compute.amazonaws.com/#/" style="font-weight: bold;">
              FindYourTourGuide
            </a>
          </p>
          <p style="font-size:14px;">
            User name: %s
          </p>
          <p style="font-size:14px;">
            Password: %s
          </p>
          <p style="font-size:14px;">
            Sincerely,
          </p>
          <p style="font-size:14px;">
            The 
            <span style="font-weight: bold;">
              FindYourTourGuide
            </span>
            Team.
          </p>
        </body>
      </html>
  """ %(user.firstName, user.userName, user.password))
      emailResult = send_html_email(user.email,html, subject) 
      session.remove()
      status = 'success'
    else:
      status = 'There is no user with this email address'
      session.remove()
      return jsonify({'result': status})
  except:
    session.remove()
    status = 'An error encountered while searching the user, please try again later'
    return jsonify({'result': status})
  return jsonify({'result': status, 'emailSent': emailResult})

# Check if there is someone logged in
@app.route('/checkLoginStatus', methods=['GET'])
def checkLoginStatus():
  if login_session:
    status = True
  else:
    status = False
  return jsonify({'result': status})

# Check if there is someone logged in - if there is return user data
@app.route('/getUserLogin', methods=['GET'])
def getUserLogin():
  status = ''
  if login_session:
    status = 'true'
    if app.db.query(User).filter(User.id == login_session['user_id']).scalar():
	    user = app.db.query(User).filter(User.id == login_session['user_id']).one()
	    session.remove()
    	    return jsonify({'result': status, 'userName': login_session['username'],
      	    'userId': login_session['user_id'], 'userType': user.userType})
    else:
	session.remove()
	status = 'false'
  else:
    session.remove()
    status = 'false'
  return jsonify({'result': status})

# Save guide details - age, certificate, years of experience and description
@app.route('/newGuideDetails', methods=['POST'])
def newGuideDetails():
  json_data = request.json
  status = ''
  user_id = json_data['userId']
  print(user_id)
  try:
      if not app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user_id,\
     	 UserPropertyAssigned.propertyId != getPropDescription()).first():
		print("I start")
        	newDescriptionPropertyAssigned = UserPropertyAssigned(
          		propertyId = getPropDescription(), userId = user_id, propertyValue = json_data['description'])

        	newAgePropertyAssigned = UserPropertyAssigned(
          		propertyId = getPropAge(), userId = user_id, propertyValue = json_data['age'])

        	newYearsOfExperiencePropertyAssigned = UserPropertyAssigned(
          		propertyId = getPropyearsOfExperience(), userId = user_id, propertyValue = json_data['yearsOfExperience'])

        	newCertificatePropertyAssigned = UserPropertyAssigned(
          		propertyId = getPropcertificate(), userId = user_id, propertyValue = json_data['certificate'])
        	
		app.db.add(newDescriptionPropertyAssigned)
        	app.db.add(newAgePropertyAssigned)
        	app.db.add(newYearsOfExperiencePropertyAssigned)
        	app.db.add(newCertificatePropertyAssigned)

        	app.db.commit()
        	status = 'success'
        	session.remove()
		print("I finish")
        	return jsonify({'result': status, 'userId': user_id})    
      else:
	    status = 'These details are allready defined for this user!'
  except:
        status = 'An error encountered while creating the user, please try again later'
  session.remove()
  return jsonify({'result': status})

# Edit and update guide details
@app.route('/updateGuideDetails', methods=['POST'])
def updateGuideDetails():
    json_data = request.json
    status = ''
    try:
    	user = app.db.query(User).filter(User.id == json_data['userId']).one()
        
	if app.db.query(UserPropertyAssigned).\
        filter(UserPropertyAssigned.propertyId == getPropcertificate()\
        ,UserPropertyAssigned.userId == json_data['userId']).scalar():

    		certificate = app.db.query(UserPropertyAssigned).\
    		filter(UserPropertyAssigned.propertyId == getPropcertificate()\
        	,UserPropertyAssigned.userId == json_data['userId']).one()
		certificate.propertyValue = json_data['certificate']
	else:
		certificate = UserPropertyAssigned(
                        propertyId = getPropcertificate(), userId = json_data['userId'], propertyValue = json_data['certificate'])

	if app.db.query(UserPropertyAssigned).\
        filter(UserPropertyAssigned.propertyId == getPropAge()\
        ,UserPropertyAssigned.userId == json_data['userId']).scalar():

                age = app.db.query(UserPropertyAssigned).\
                filter(UserPropertyAssigned.propertyId == getPropAge()\
                ,UserPropertyAssigned.userId == json_data['userId']).one()
                age.propertyValue = json_data['age']
        else:
                age = UserPropertyAssigned(
                        propertyId = getPropAge(), userId = json_data['userId'], propertyValue = json_data['age'])

	
	if app.db.query(UserPropertyAssigned).\
        filter(UserPropertyAssigned.propertyId == getPropyearsOfExperience()\
        ,UserPropertyAssigned.userId == json_data['userId']).scalar():

    		yearsOfExperience = app.db.query(UserPropertyAssigned).\
        	filter(UserPropertyAssigned.propertyId == getPropyearsOfExperience()\
        	,UserPropertyAssigned.userId == json_data['userId']).one()
		yearsOfExperience.propertyValue = json_data['years']
	else:
		yearsOfExperience = UserPropertyAssigned(
                        propertyId = getPropyearsOfExperience(), userId = json_data['userId'], propertyValue = json_data['years'])

	if  app.db.query(UserPropertyAssigned).\
        filter(UserPropertyAssigned.propertyId == getPropDescription()\
        ,UserPropertyAssigned.userId == json_data['userId']).scalar():

        	description = app.db.query(UserPropertyAssigned).\
        	filter(UserPropertyAssigned.propertyId == getPropDescription()\
        	,UserPropertyAssigned.userId == json_data['userId']).one()
		description.propertyValue = json_data['descrip']
	else:
		description = UserPropertyAssigned(
                        propertyId = getPropDescription(), userId = json_data['userId'], propertyValue = json_data['descrip'])
		

        emailExist = app.db.query(User).\
        filter(json_data['email'] == User.email, User.id != json_data['userId']).scalar()

        if emailExist:
      		status = 'The email is allrdeay assigned to another user!'
      		return jsonify({'result': status})
      
        user.firstName = json_data['firstName']
        user.lastName = json_data['lastName']
        user.email = json_data['email']
	if json_data['email'] or json_data['firstName'] or json_data['lastName']:
        	app.db.add(user)
		app.db.commit()
	if json_data['certificate']:
		app.db.add(certificate)
	if json_data['years']:
		app.db.merge(yearsOfExperience)
	if  json_data['descrip']:
		app.db.merge(description)
	if json_data['age']:
		app.db.merge(age)
        app.db.commit()            
	usersData = app.db.query(User.id, User.userName, User.firstName, User.lastName, UserPropertyAssigned.propertyValue, Properties.propertyName).\
	 filter(User.id == UserPropertyAssigned.userId, UserPropertyAssigned.propertyId == Properties.id, User.id == json_data['userId']).all()
	session.remove()
    except:
	session.remove()
    	status = 'An error encountered while updating the user data, please try again later'
    return jsonify({'result': status})


@app.route('/uploadFile/<int:user_id>', methods=['POST'])
def uploadFile(user_id):
  file = request.files['file']
  status = ''
  if not app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user_id,\
     UserPropertyAssigned.propertyId == getPropPhoto()).first():
  	    #try:
            if allowed_file(file.filename):
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		print("I save photo")
        	newPhotoPropertyAssigned = UserPropertyAssigned(
            	propertyId = getPropPhoto(), userId = user_id, propertyValue = file.filename)
        	app.db.add(newPhotoPropertyAssigned)
        	app.db.commit()
		print("I save th photo in the DB")
        	session.remove()
      		status = 'success'
		print("I finish")
	    else:
		session.remove()
        	status = 'Please choose a file from type jpg / jpeg / png'
            #except:
	    #session.remove()
     	    #status = 'An error encountered while saving the user photo, please try again later'
  else:
	session.remove()
	status = 'There is allready a photo for this guide'
  return jsonify({'result': status})

# Change and update guide photo
@app.route('/updateFile/<int:user_id>', methods=['POST'])
def updateFile(user_id):
    file = request.files['file']
    status = ''
    try:  
	print("updating file")
    	userPhoto = app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user_id,\
      		UserPropertyAssigned.propertyId == getPropPhoto()).one()
    	if allowed_file(file.filename):
		print("file name is ok")
	        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		# os.remove(os.path.join(app.config['UPLOAD_FOLDER'], userPhoto.propertyValue))
		print("I saved file")
        	userPhoto.propertyValue = file.filename
        	app.db.merge(userPhoto)
		print("I added file to session")
        	app.db.commit()
        	session.remove()
		print("finish updating file")
        	status = 'success'
	else:
                session.remove()
		status = 'Please choose a file from type from type jpg / jpeg / png'
    except:
	session.remove()
        status = 'An error encountered while updating the photo, please try again later'
    return jsonify({'result': status})


# Add a new language to the list of languages in which the user can guide
@app.route('/addLanguange', methods=['POST'])
def addLanguange():
  json_data = request.json
  status = ''
  try:
    userHasLanguage = app.db.query(GuideLanguage).\
      filter(GuideLanguage.languageName == json_data['language'], GuideLanguage.userId == json_data['userId']).\
      scalar()
    if not userHasLanguage:
      newGuideLanguage = GuideLanguage(languageName = json_data['language'], userId = json_data['userId'])
      app.db.add(newGuideLanguage)
      app.db.commit()
      session.remove()
      status = 'success'
    else:
      status = 'You allready chose this language, please choose a new language or continue!'
  except:
        status = 'An error encountered while creating the user, please try again later'
  return jsonify({'result': status})

# Remove a language from the lis of languages in which the user can guide
@app.route('/removeLanguage', methods=['POST'])
def removeLanguage():
  json_data = request.json
  status = ''
  userLanguage = app.db.query(GuideLanguage).\
  filter(GuideLanguage.languageName == json_data['language'], GuideLanguage.userId == json_data['userId']).\
  one()
  try:
      app.db.delete(userLanguage)
      app.db.commit()
      session.remove()
      status = 'success'
  except:
	session.remove()
        status = 'An error encountered while updating the user, please try again later'
  return jsonify({'result': status})  

# Get all languages in whic the user can guide
@app.route('/getLanguanges/<int:user_id>/', methods=['GET'])
def getLanguanges(user_id):
  status = ''
  try:
    languages = app.db.query(GuideLanguage).filter(GuideLanguage.userId == user_id).all()
    status = 'success'
    session.remove()
  except:
      status = 'An error encountered while geting the data, please try again later'
      return jsonify({'result': status})
      session.remove()
  return jsonify(languages=[i.serialize for i in languages]) 

# Add a location where the guide performs tours
@app.route('/addLocation', methods=['POST'])
def addLocation():
  json_data = request.json
  status = ''
  try:
    hasLocation = app.db.query(GuideLocations).filter(GuideLocations.userId == json_data['userId'],\
      GuideLocations.location == json_data['location']).scalar()
    if not hasLocation:
      newGuideLoc = GuideLocations(userId = json_data['userId'], location = json_data['location'])
      app.db.add(newGuideLoc)
      app.db.commit()
      session.remove()
      status = 'success'
    else:
      status = 'You allready chose this location, please choose a new location or continue!'
  except:
    status = 'An error encountered while saving the data, please try again later'
  return jsonify({'result': status})

# Remove a location from the list of locations in which the guide can guide
@app.route('/removeLocation', methods=['POST'])
def removeLocation():
  json_data = request.json
  status = ''
  try:
    guideLoc = app.db.query(GuideLocations).\
      filter(GuideLocations.userId == json_data['userId'],\
      GuideLocations.location == json_data['location']).one()
    app.db.delete(guideLoc)
    app.db.commit()
    session.remove()
    status = 'success'
  except:
    session.remove()
    status = 'An error encountered while updaing the user data, please try again later'
  return jsonify({'result': status}) 

# Get the list of locations in which the guide can guide
@app.route('/getGuideLocations/<int:user_id>', methods=['GET'])
def getGuideLocations(user_id):
  status = ''
  try:
    status = 'success'
    guideLocs = app.db.query(GuideLocations).filter(GuideLocations.userId == user_id).all()
    session.remove()
  except:
    session.remove()
    status = 'An error encountered while geting the data, please try again later'
    return jsonify({'result': status}) 
  return jsonify(guideLocs=[i.serialize for i in guideLocs])


# Delete a range of dates from the list of dates in which the guide is busy
@app.route('/ClearBusyDates', methods=['POST'])
def ClearBusyDates():
  json_data = request.json
  status = ''
  try:
    guideAvail = app.db.query(GuideBusyDates).\
      filter(GuideBusyDates.userId == json_data['userId']).all()
    for guideA in guideAvail:
      if (guideA.startDate.strftime('%d-%m-%Y') == json_data['fromDate'] 
      and guideA.endDate.strftime('%d-%m-%Y') == json_data['toDate']):
        app.db.delete(guideA)
    app.db.commit()
    session.remove()
    status = 'success'
  except:
    session.remove()
    status = 'An error encountered while updaing the user availability, please try again later'
  return jsonify({'result': status}) 

# Get the list of dates in which the guide is busy
@app.route('/getGuideAvailability/<int:user_id>', methods=['GET'])
def getGuideAvailability(user_id):
  status = ''
  try:
    status = 'success'
    guideAvail = app.db.query(GuideBusyDates).filter(GuideBusyDates.userId == user_id).all()
    session.remove()
  except:
    session.remove()
    status = 'An error encountered while geting the data, please try again later'
    return jsonify({'result': status}) 
  return jsonify(guideAvail=[i.serialize for i in guideAvail])


# Add a new range of dates in which the guide is busy
@app.route('/updateGuideAvailability', methods=['POST'])
def updateGuideAvailability():
  json_data = request.json
  status = ''
  guideAllreadyBusy = ''
  try:  
    guideAvail = app.db.query(GuideBusyDates).\
      filter(GuideBusyDates.userId == json_data['userId']).all()   
    for guideA in guideAvail:
      if (guideA.startDate.strftime('%d-%m-%Y') == json_data['fromDate'] 
      and guideA.endDate.strftime('%d-%m-%Y') == json_data['toDate']):
        guideAllreadyBusy = True
    if not guideAllreadyBusy:
      guideAvail = GuideBusyDates(userId = json_data['userId'],\
        startDate = datetime.strptime(json_data['fromDate'], '%d-%m-%Y'),\
        endDate = datetime.strptime(json_data['toDate'], '%d-%m-%Y'))
      app.db.add(guideAvail)
      app.db.commit()
      session.remove()
      status = 'success'
    else:
      status = 'You allready chose these dates, please choose new dates or continue!'
  except:
    status = 'An error encountered while geting the data, please try again later'
  session.remove()
  return jsonify({'result': status}) 

# Add a review to a guide
@app.route('/addReview', methods=['POST'])
def addReview():
    json_data = request.json
    success = ''
    try:
        newReview = Reviews(userIdWriter = json_data['writerUserId'], 
          userIdReceiver = json_data['recieverUserId'], content = json_data['review'],
          grade=json_data['reviewGrade'], headline = '1')
        app.db.add(newReview)
        app.db.commit()
        session.remove()
        status = 'success'
    except:
      status = 'An error accoured while saving the reveiw, please try again later!'
    session.remove()
    return jsonify({'result': status}) 

# Write a private messgae to a guide
# An email will be sent to the user saying that there is amessgae waiting for him
@app.route('/writeMessage', methods=['POST'])
def writeMessage():
  json_data = request.json
  success = ''
  try:
      newChat = PrivateChat(userIdWriter = json_data['writer'], userIdReceiver = json_data['receiver'],
       content = json_data['msgContent'], headline = json_data['msgTitle'])
      app.db.add(newChat)
      app.db.commit()
      user = app.db.query(User).filter(User.id == json_data['receiver']).one()
      subject = 'A new message is waiting for you in \'Find Your Tour Guide\''
      html = ("""
      <html style="font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif">
        <head></head>
        <body>
          <p style="font-size:18px; font-weight: bold;">
            Hello %s
          </p> 
          <p style="font-size:14px;">
            There is a new message waiting for you in 
            <a href="http://ec2-52-36-140-206.us-west-2.compute.amazonaws.com/#/" style="font-weight: bold;">
              FindYourTourGuide
            </a>
          </p>
          <p style="font-size:14px;">
            Sincerely,
          </p>
          <p style="font-size:14px;">
            The 
            <span style="font-weight: bold;">
              FindYourTourGuide
            </span>
            Team.
          </p>
        </body>
      </html>
  """ %user.firstName)
      emailResult = send_html_email(user.email,html, subject)
      session.remove()
      status = 'success'
  except:
	status="An error occurred, please try again later"
  session.remove()
  return jsonify({'result': status, 'emailSent': emailResult}) 

# Get all private messages between 2 users
@app.route('/getMessagesBetweenUsers/<int:user_id1>/<int:user_id2>', methods=['GET'])
def getMessagesBetweenUsers(user_id1, user_id2):
  try:
    user1 = app.db.query(User.userName, User.email, User.id).filter(User.id == user_id1).one()        
    user2 = app.db.query(User.userName, User.email, User.id).filter(User.id == user_id2).one()        
    chat = app.db.query(PrivateChat).\
      filter(PrivateChat.userIdWriter.in_([user_id1,user_id2]), PrivateChat.userIdReceiver.\
        in_([user_id1,user_id2])).order_by(desc(PrivateChat.timestmp)).all() 
    session.remove()
    return jsonify(chat=[i.serialize for i in chat], user1 = {'userName': user1.userName, 'id': user_id1}
      ,user2 ={'userName': user2.userName, 'id': user_id2})
  except:
    session.remove()
    status = 'An error accoured while getting the messages, please try again later!'
    return jsonify({'result': status})

# Get all user that a specific user had private chats with
@app.route('/privateChat/<int:user_id>/', methods=['GET'])
def privateChat(user_id):
  try:     
    users = app.db.query(distinct(User.userName), User.id).\
      filter(User.id.in_([PrivateChat.userIdWriter, PrivateChat.userIdReceiver]) \
      ,or_(PrivateChat.userIdWriter == user_id, PrivateChat.userIdReceiver == user_id))
    chatUsers = []  
    for user in users:
      if user.id != user_id:
        chatUsers.append({'userName': user[0], 'id': user[1]})
    session.remove()
    return jsonify({'chatUsers': chatUsers})
  except:
    session.remove()
    status = 'An error accoured while getting the messages, please try again later!'
    return jsonify({'result': status})
      
# Search by location
@app.route('/search/<string:search_data>/', methods=['GET'])
def search(search_data):
  status = ''
  guides = []
  checkUsers = []
  try:
      if search_data.find(",") >= 0:
        locations = search_data.split(",")
        for location in locations:
          print(location)
          users = app.db.query(User).\
          filter(User.userType == 'G', User.id == GuideLocations.userId,\
            func.lower(GuideLocations.location).contains(location.lower())).all()
          print("locs found")
          print(users)
        for user in users:
          newUser = True
          for cu in checkUsers:
            if user.id == cu.id:
              newUser = False
          if newUser:
            checkUsers.append(user)  
      else:
        location = search_data
        users = app.db.query(User).\
          filter(User.userType == 'G', User.id == GuideLocations.userId,\
            func.lower(GuideLocations.location).contains(location.lower())).all()
        print("locs found for one string")
        print(users)
        for user in users:
          newUser = True
	  print(user.userName, user.id)
          for cu in checkUsers:
            if user.id == cu.id:
              newUser = False
          if newUser:
            checkUsers.append(user)
      for user in checkUsers:
        totalGrade = 0
        avgGrade = 0
        numOfReviews = 0
        locs = []
        langs = []
        hasPhoto = app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user.id,\
        UserPropertyAssigned.propertyId == getPropPhoto()).first()
        if hasPhoto:
          photo = app.db.query(UserPropertyAssigned).\
            filter(UserPropertyAssigned.propertyId == getPropPhoto(), UserPropertyAssigned.userId == user.id).one() 
          if app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).first():
            guideLocs = app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).all()
            for gl in guideLocs:
              location = {'location': gl.location}
              locs.append(location) 

          if app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).first():
            languages = app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).all()
            for lang in languages:
              lan = {'languageName': lang.languageName}
              langs.append(lan)

          if app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).first():
            reviews = app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).all()
            
            for rev in reviews:
              totalGrade = totalGrade + rev.grade;
              numOfReviews = numOfReviews + 1 
          if numOfReviews > 0:
            avgGrade = totalGrade/numOfReviews

          guide = {'firstName': user.firstName, 'lastName': user.lastName, 'userId': user.id,
            'photo': photo.propertyValue, 'grade': avgGrade,
            'numOfReviews': numOfReviews, 'locs': locs, 'langs': langs}
          guides.append(guide)

      status = 'success'  
      session.remove() 
  except:
      status = 'An error encountered while geting the user name and Properties, please try again later'
      return jsonify({'result': status})
  return jsonify({'guides': guides})
      
# Get search results for for advanced search
# Search by country, city, language and dates

@app.route('/advancedSearch/<string:location>/<string:language>/<string:fromDate>/<string:toDate>', methods=['GET'])
def advancedSearch(location,language,fromDate,toDate):
    status = ''
    guides = []
    checkUsers = []
    try:

      if location != 'noLocation' and language != 'noLanguage':
        
        if location.find(",") >= 0:
          locations = location.split(",")
          for location in locations:
            print(location)
            users = app.db.query(User).\
            filter(User.userType == 'G', User.id == GuideLocations.userId,\
              func.lower(GuideLocations.location).contains(location.lower()),\
              GuideLanguage.userId == User.id, GuideLanguage.languageName == language).all()
            print("locs found")
            print(users)
          for user in users:
            newUser = True
            for cu in checkUsers:
              if user.id == cu.id:
                newUser = False
            if newUser:
              checkUsers.append(user)  
        else:
          users = app.db.query(User).\
            filter(User.userType == 'G', User.id == GuideLocations.userId,\
              func.lower(GuideLocations.location).contains(location.lower()),\
              GuideLanguage.userId == User.id, GuideLanguage.languageName == language).all()
          print("locs found")
          print(users)
          for user in users:
            newUser = True
            for cu in checkUsers:
              if user.id == cu.id:
                newUser = False
            if newUser:
              checkUsers.append(user)


      if location != 'noLocation' and language == 'noLanguage':
        
        if location.find(",") >= 0:
          locations = location.split(",")
          for location in locations:
            print(location)
            users = app.db.query(User).\
            filter(User.userType == 'G', User.id == GuideLocations.userId,\
              func.lower(GuideLocations.location).contains(location.lower())).all()
            print("locs found")
            print(users)
          for user in users:
            newUser = True
            for cu in checkUsers:
              if user.id == cu.id:
                newUser = False
            if newUser:
              checkUsers.append(user)  
        else:
          users = app.db.query(User).\
            filter(User.userType == 'G', User.id == GuideLocations.userId,\
              func.lower(GuideLocations.location).contains(location.lower())).all()
          print("locs found")
          print(users)
          for user in users:
            newUser = True
            for cu in checkUsers:
              if user.id == cu.id:
                newUser = False
            if newUser:
              checkUsers.append(user)

      if location == 'noLocation' and language != 'noLanguage':
        checkUsers = app.db.query(User).\
          filter(User.userType == 'G', GuideLanguage.userId == User.id,\
          GuideLanguage.languageName == language).all()

      if location == 'noLocation' and language == 'noLanguage':
        checkUsers = app.db.query(User).filter(User.userType == 'G').all()

      for user in checkUsers:
        totalGrade = 0
        avgGrade = 0
        numOfReviews = 0
        locs = []
        langs = []
        isGuideManageAvail = app.db.query(exists().where(GuideBusyDates.userId == user.id)).scalar()
        hasPhoto = app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user.id,\
          UserPropertyAssigned.propertyId == getPropPhoto()).first()
        if not isGuideManageAvail:
          if hasPhoto:
            photo = app.db.query(UserPropertyAssigned).\
              filter(UserPropertyAssigned.propertyId == getPropPhoto(), UserPropertyAssigned.userId == user.id).one() 
            if app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).first():
              guideLocs = app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).all()
              for gl in guideLocs:
                location = {'location': gl.location}
                locs.append(location) 

            if app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).first():
              languages = app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).all()
              for lang in languages:
                lan = {'languageName': lang.languageName}
                langs.append(lan)

            if app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).first():
              reviews = app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).all()
              
              for rev in reviews:
                totalGrade = totalGrade + rev.grade;
                numOfReviews = numOfReviews + 1 
              if numOfReviews > 0:
                avgGrade = totalGrade/numOfReviews

            guide = {'firstName': user.firstName, 'lastName': user.lastName, 'userId': user.id,
              'photo': photo.propertyValue, 'grade': avgGrade,
              'numOfReviews': numOfReviews, 'locs': locs, 'langs': langs}
            guides.append(guide)

        if isGuideManageAvail:
          guideBusy = app.db.query(GuideBusyDates).filter(GuideBusyDates.userId == user.id).all()
          guideAvailInDates = True
          for gb in guideBusy:
            isGuideBusy = ((datetime.strptime(fromDate, '%d-%m-%Y').date() <= gb.startDate 
              and datetime.strptime(fromDate, '%d-%m-%Y').date() >= gb.endDate) 
              or (datetime.strptime(toDate, '%d-%m-%Y').date() >= gb.startDate
              and datetime.strptime(toDate, '%d-%m-%Y').date() <= gb.endDate)
              or (datetime.strptime(fromDate, '%d-%m-%Y').date() <= gb.startDate 
              and datetime.strptime(toDate, '%d-%m-%Y').date() >= gb.endDate))

            if isGuideBusy:
              guideAvailInDates = False

          if guideAvailInDates:
            if hasPhoto:
              photo = app.db.query(UserPropertyAssigned).\
                filter(UserPropertyAssigned.propertyId == getPropPhoto(), UserPropertyAssigned.userId == user.id).one() 
              
              if app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).first():
                guideLocs = app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).all()
                for gl in guideLocs:
                  location = {'location': gl.location}
                  locs.append(location)

              if app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).first():
                languages = app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).all()
                for lang in languages:
                  lan = {'languageName': lang.languageName}
                  langs.append(lan)

              if app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).first():
                reviews = app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).all()
              
                for rev in reviews:
                  totalGrade = totalGrade + rev.grade;
                  numOfReviews = numOfReviews + 1 
                
                if numOfReviews > 0:
                  avgGrade = totalGrade/numOfReviews

              guide = {'firstName': user.firstName, 'lastName': user.lastName, 'userId': user.id,
                'photo': photo.propertyValue, 'grade': avgGrade,
                'numOfReviews': numOfReviews, 'locs': locs, 'langs': langs}
              guides.append(guide)

      status = 'success'
      session.remove()  
    except:
      status = 'An error encountered while geting the user name and Properties, please try again later'
      return jsonify({'result': status})
    return jsonify({'guides': guides})


# Get guide profile
@app.route('/getGuideProfile/<int:user_id>', methods=['GET'])
def getGuideProfile(user_id):
  status = ''
  try:
    desc = ''
    age = ''
    years = ''
    photo = ''
    certificate = ''
    user = app.db.query(User).filter(User.id == user_id).one()
    if app.db.query(UserPropertyAssigned).\
      filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropDescription()).first():
    	desc = app.db.query(UserPropertyAssigned.propertyValue).\
      	filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropDescription()).one() 
    if app.db.query(UserPropertyAssigned).\
      filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropAge()).first():
    	age = app.db.query(UserPropertyAssigned.propertyValue).\
      	filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropAge()).one()
    if app.db.query(UserPropertyAssigned).\
      filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropyearsOfExperience()).first():
    	years = app.db.query(UserPropertyAssigned.propertyValue).\
      	filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropyearsOfExperience()).one()
    if app.db.query(UserPropertyAssigned).\
      filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropcertificate()).first():
    	certificate = app.db.query(UserPropertyAssigned.propertyValue).\
      	filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropcertificate()).one()	
    if  app.db.query(UserPropertyAssigned).\
      filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropPhoto()).first():
    	photo = app.db.query(UserPropertyAssigned.propertyValue).\
      	filter(UserPropertyAssigned.userId == user_id, UserPropertyAssigned.propertyId == getPropPhoto()).one()

    status = 'success'  
    session.remove()
  except:
    session.remove()
    status = 'An error encountered while getting the user name and Properties, please try again later'
    return jsonify({'result': status}) 
  return jsonify({'firstName': user.firstName, 'lastName': user.lastName,'desc': desc,
   'age': age, 'years': years, 'certificate': certificate,
   'email': user.email, 'photo': photo})

# Get all reviews that were written for a guide
@app.route('/getReviews/<int:user_id>', methods=['GET'])
def getReviews(user_id):
  status = ''
  try:
    reviews = app.db.query(Reviews).filter(Reviews.userIdReceiver == user_id).all()
    users = app.db.query(User).filter(or_(User.id == Reviews.userIdReceiver, User.id == Reviews.userIdWriter)).all()
    status = 'success'
    session.remove()  
  except:
    status = 'An error encountered while geting the guide reviews, please try again later'
    return jsonify({'result': status}) 
  session.remove()
  return jsonify(reviews=[i.serialize for i in reviews], users=[i.serialize for i in users])

# Get all guides data
@app.route('/getGuides', methods=['GET'])
def getGuides():
   status = ''
   guides = []
   #try:
   if app.db.query(User).filter(User.userType == 'G').first():
    users = app.db.query(User).filter(User.userType == 'G').all()
    for user in users:
      totalGrade = 0
      avgGrade = 0
      numOfReviews = 0
      locs = []
      langs = []
      hasDesc = app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user.id,\
      UserPropertyAssigned.propertyId == getPropDescription()).first()
      hasPhoto = app.db.query(UserPropertyAssigned).filter(UserPropertyAssigned.userId == user.id,\
      UserPropertyAssigned.propertyId == getPropPhoto()).first()
      
      if hasPhoto and hasDesc:
        desc = app.db.query(UserPropertyAssigned).\
          filter(UserPropertyAssigned.propertyId == getPropDescription(),\
          UserPropertyAssigned.userId == user.id).one()
        photo = app.db.query(UserPropertyAssigned).\
          filter(UserPropertyAssigned.propertyId == getPropPhoto(),\
          UserPropertyAssigned.userId == user.id).one()
        
        if app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).first():
          guideLocs = app.db.query(GuideLocations).filter(GuideLocations.userId == user.id).all()
          for gl in guideLocs:
            location = {'location': gl.location}
            locs.append(location) 

        if app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).first():
          languages = app.db.query(GuideLanguage).filter(GuideLanguage.userId == user.id).all()
          for lang in languages:
            lan = {'languageName': lang.languageName}
            langs.append(lan) 

        if app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).first():
          reviews = app.db.query(Reviews).filter(Reviews.userIdReceiver == user.id).all()
          
          for rev in reviews:
            totalGrade = totalGrade + rev.grade;
            numOfReviews = numOfReviews + 1 
          avgGrade = totalGrade/numOfReviews
        guide = {'firstName': user.firstName, 'lastName': user.lastName, 'userId': user.id,
          'desc': desc.propertyValue, 'photo': photo.propertyValue, 'grade': avgGrade,
          'numOfReviews': numOfReviews, 'locs': locs, 'langs': langs}
        guides.append(guide)
 
    status = 'success'
    session.remove() 
    #except:
    #status = 'An error encountered while geting the user name and Properties, please try again later'
    #return jsonify({'result': status}) 
    session.remove()
    return jsonify({'guides': guides})
    

  
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # If debug is enabled, the server will reload itself each time it notices a
    # code change.
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
