#/app dir is where the application package lives
#this is the init script for our app package

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__) #app the variable
app.config.from_object('config') #read config from config.py
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
lm.login_view = 'login' #allows redirect to login view

#views module needs to import app the variable, so we define this
#import after declaring the variable
from app import views, models #app the package


#Email logging
if not app.debug:
  import logging
  from logging.handlers import SMTPHandler
  credentials = None
  if MAIL_USERNAME or MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
  mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'mblog failure', credentials)
  mail_handler.setLevel(logging.ERROR)
  app.logger.addHandler(mail_handler)

#File Logging

# log file goes into tmp dir with name mblog.log
# RotatingFileHandler limits the amount of logs generated (max file size 1MB and keep the last 10 logs)
# logging.Formatter provides custom formatting for log messages:
# * timestamp
# * logging level
# * file
# * linenumber
# * log message
# * stack trace

# To make logging more useful we have lowered the logging level in both the app logger and the file logger handler.  Means we can write useful messages to the log without calling them errors.  E.g.

#   We log the app starting up as an informational level

if not app.debug:
  import logging
  from logging.handlers import RotatingFileHandler
  file_handler = RotatingFileHandler('tmp/mblog.log', 'a', 1 * 1024 * 1024, 10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('mblog startup')
