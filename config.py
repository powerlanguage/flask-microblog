import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Cross site request forgery prevention
WTF_CSRF_ENABLED = True

SECRET_KEY = 'ajsfbsfjbaSFJSAF'

OPENID_PROVIDERS = [
  {'name': 'Google', 'url': 'https://www.google.com/accountso8/id'},
  {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
  {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
  {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
  {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

#mail server settings
#used for emailing errors
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

#administrator list
ADMINS = ['josh@powerlanguage.co.uk']



