from app import app #from app the package import app the variable, i think
from flask import render_template, flash, redirect
from .forms import LoginForm #not sure what the . is about

@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'JDub'} #fake user
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
def login():
  form = LoginForm()
  #will validate as False with no data, so the form will be rendered
  #if validates successfully will redirect
  #if doesn't validate will render form again
  if form.validate_on_submit():
      flash('Login request from OpenID="%s", remember_me=%s' %
        (form.openid.data, str(form.remember_me.data)))
      return redirect('/index')
  return render_template(
    'login.html',
    title='Sign In',
    form=form,
    providers=app.config['OPENID_PROVIDERS']
  )

