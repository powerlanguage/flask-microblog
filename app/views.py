from app import app #from app the package import app the variable, i think
from flask import render_template

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
