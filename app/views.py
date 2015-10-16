from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

#from app the package import app the variable, i think
from app import app, db, lm, oid

#not sure what the . is about
from .forms import LoginForm, EditForm
from .models import User

from datetime import datetime

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/')
@app.route('/index')
@login_required
def index():
  user = g.user
  posts = [ #fake array of posts
    {
      'author': {'nickname': 'John'},
      'body': 'A beautiful day in PDX'
    },
    {
      'author': {'nickname': 'Susan'},
      'body': "The avengers was so cool!"
    }
  ]
  return render_template('index.html',
                          title='Home',
                          user=user,
                          posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler #tells Flask-OpenID that this is our login view function
def login():
  if g.user is not None and g.user.is_authenticated: #g is global
    return redirect(url_for('index'))
  form = LoginForm()
  #will validate as False with no data, so the form will be rendered
  #if validates successfully will redirect
  #if doesn't validate will render form again
  if form.validate_on_submit():
      #store boolean in flask session
      session['remember_me'] = form.remember_me.data
      return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
  return render_template(
    'login.html',
    title='Sign In',
    form=form,
    providers=app.config['OPENID_PROVIDERS']
  )

#resp arg contains information return by the OpenID provided

@oid.after_login
def after_login(resp):
  #require an email to login
  if resp.email is None or resp.email == "":
    flash('Invalid login.  Try again.')
    return redirect(url_for('login'))
  #search db for the email provided
  #if not found, this is a new user, add to DB
  user = User.query.filter_by(email=resp.email).first()
  if user is None:
    nickname = resp.nickname
    if nickname is None or nickname == "":
      nickname = resp.email.split('@')[0]
    user = User(nickname=nickname, email=resp.email)
    db.session.add(user)
    db.session.commit()
  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)
  login_user(user, remember = remember_me)
  return redirect(request.args.get('next') or url_for('index'))


#Any functions that are decorated with before_request will run before the view function each time a request is received.
@app.before_request
def before_request():
  #takes current-user set by Flask-Login and put into global g
  g.user = current_user

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

#argument passed into the route decorator will be passed to the function
@app.route('/user/<nickname>')
@login_required
def user(nickname):
  user = User.query.filter_by(nickname=nickname).first()
  if user == None:
    flash('User {} not found'.format(nickname))
    return redirect(url_for('index'))
  posts = [
    {'author': user, 'body': 'Test post #1'},
    {'author': user, 'body': 'Test post #2'}
  ]
  return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
  form = EditForm()
  if form.validate_on_submit():
    g.user.nickname = form.nickname.data
    g.user.about_me = form.about_me.data
    db.session.add(g.user)
    db.session.commit()
    flash("Your changes have been saved")
    return redirect(url_for('edit'))
  else:
    form.nickname.data = g.user.nickname
    form.about_me.data = g.user.about_me
  return render_template('edit.html', form=form)
