from flask import Flask

app = Flask(__name__) #app the variable
app.config.from_object('config') #read config from config.py

from app import views #app the package
