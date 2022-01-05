import datetime
import pickle
from flask import Flask
import flask_sqlalchemy
from sqlalchemy.sql.expression import desc
from flask_sqlalchemy import SQLAlchemy
import app
import pytest
from models import *
from hashlib import sha256

app = Flask(__name__)
app.secret_key = '60a725867b515697115ccb2c561c2fee5694f2bc0d96372a4a033880702fa4a4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#def test_has_voted():
 #   has_voted=Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).count() > 0
  #  assert 

def test_register():
    name = "jean"
    surname ="eude"
    email = "jean@eude.com"
    password = "password"

    hash = sha256()
    hash.update(password.encode('utf-8'))
    hashed_pwd = hash.hexdigest() 
    db_user = User(password_hash=hashed_pwd, email=email, name=name, surname=surname, role='Citoyen', statut='User')
    assert db_user.name == "jean"
    assert db_user.surname =="eude"
    assert db_user.email =="jean@eude.com"
    assert db_user.password_hash != "password"

