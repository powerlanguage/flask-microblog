#/app dir is where the application package lives
#this is the init script for our app package

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

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
