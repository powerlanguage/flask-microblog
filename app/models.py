from app import db

# creating instances of the db.Column which takes field type as argument

class User(db.model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)

  def __repr__(self):
    return '<User %r>' % (self.nickname)
