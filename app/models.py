from app import db
from hashlib import md5 #using for gravatar

#No declaring this table as a model like we did for users and posts. since this is
# an auxillary table that has no data other than the foreign keys we use lower level
#apis to create the table without an associated model
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
  )

# creating instances of the db.Column which takes field type as argument
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime)
                              #right side entity, parent class is left
  followed = db.relationship('User',
                              #indicates association table used in relationship
                              secondary=followers,
                              #the condition that links left side (follower) to the
                              #association table
                              primaryjoin=(followers.c.follower_id == id),
                              #the condition that links right side (followed) to the
                              #association table
                              secondaryjoin=(followers.c.followed_id == id),
                              #defines relationship as accesssed from the right side
                              #followed returns users following current user
                              #followers returns users followed by current user
                              backref=db.backref('followers', lazy='dynamic'),
                              lazy='dynamic')

  #returns an object when it succeeds or None when it fails
  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)
      return self

  #returns an object when it succeeds or None when it fails
  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)
      return self

  def is_following(self, user):
    return self.followed.filter(followers.c.followed_id == user.id).count() > 0

  @property
  def is_authenticated(self):
      return True

  @property
  def is_active(self):
      return True

  @property
  def is_anonymous(self):
      return False

  def get_id(self):
    try:
        return unicode(self.id) #python2
    except NameError:
        return str(self.id) #python3

  # https://en.gravatar.com/site/implement/images
  # md5 of email appended to URL
  # d==retro, returns grib-like avatar if they don't have one
  # s=N requests a scaled version
  def avatar(self, size):
    return 'http://www.gravatar.com/avatar/%s?d=retro&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

  #add counter to nickname until unique
  @staticmethod
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname=nickname).first() is None:
      return nickname
    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(nickname=new_nickname).first() is None:
        break
      version += 1
    return new_nickname

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post %r>' % (self.body)
