from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, abort, url_for
from hashlib import sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route('/')
def home():
    articles = Article.query.all()
    return render_template('home.html', articles=[])

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
        pwd_hash = h.hexdigest
        db_user = User.query.filter_by(email=email).first()
        if db_user is None:
            return render_template('register.html')
        db_hash = db_user.hash
        if pwd_hash != db_hash:
            return abort(406)
        else:
            return abort(418)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/project/<article_id>')
def project(article_id):
    article = Article.query.filter_by(article_id=article_id)
    return render_template('project.html', article=[])