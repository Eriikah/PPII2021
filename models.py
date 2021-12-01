from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(64))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    role = db.Column(db.String(16))
    statut = db.Column(db.String(16))