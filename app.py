from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, abort, url_for, session
from hashlib import sha256

app = Flask(__name__)
app.secret_key = '60a725867b515697115ccb2c561c2fee5694f2bc0d96372a4a033880702fa4a4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route('/')
def home():
    articles = Article.query.all()
    return render_template('home.html',articles=articles, logged_in='user_id' in session.keys(), status='status' in session.keys())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        h = sha256()
        form = request.form
        email = form.get('email')
        pwd = form.get('password')
        if not email or not pwd:
            return abort(406) # temporary
        h.update(pwd.encode('utf-8'))
        pwd_hash = h.hexdigest()
        db_user = User.query.filter_by(email=email).first()
        if db_user is None:
            return render_template('register.html', logged_in='user_id' in session.keys())
        db_hash = db_user.password_hash
        if pwd_hash != db_hash:
            return abort(406)
        else:
            session['user_id'] = db_user.user_id
            return render_template('home.html', logged_in=True)
    return render_template('login.html', logged_in='user_id' in session.keys(), status='status' in session.keys())


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', logged_in='user_id' in session.keys(), status='status' in session.keys())


@app.route('/project/<article_id>')
def project(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    return render_template('article.html', article=article, logged_in='user_id' in session.keys(), status='status' in session.keys())

@app.route('/logout')
def logout():
    session.pop('user_id')
    return render_template('home.html', logged_in='user_id' in session.keys(), status='status' in session.keys())

@app.route("/postpage")
def publier():
    
    return render_template('postpage.html', logged_in='user_id' in session.keys(), status='status' in session.keys())
