from flask import Flask

app = Flask(__name__) #app the variable
from app import views #app the package
