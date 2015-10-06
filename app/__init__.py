#/app dir is where the application package lives
#this is the init script for our app package

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__) #app the variable
app.config.from_object('config') #read config from config.py
db = SQLAlchemy(app)

#views module needs to import app the variable, so we define this
#import after declaring the variable
from app import views, models #app the package
