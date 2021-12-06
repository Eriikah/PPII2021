from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(64))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    role = db.Column(db.String(16))
    statut = db.Column(db.String(16))

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    poster_id= db.Column(db.Integer)
    title = db.Column(db.String(64))
    vote_pos = db.Column(db.Integer)
    vote_neg = db.Column(db.Integer)
    content = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    post_time = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    tag1 = db.Column(db.String(16))
    tag2 = db.Column(db.String(16))
    tag3 = db.Column(db.String(16))

class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    vote_on = db.Column(db.String(32))
    parent_id= db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_vote = db.Column(db.Integer)
    vote_time = db.Column(db.DateTime)