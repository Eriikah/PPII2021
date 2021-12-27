from flask import Flask
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, abort, url_for, session, redirect
from hashlib import sha256
from datetime import datetime
from sqlalchemy import or_

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
    return render_template('home.html',articles=articles)

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
            return redirect('/register')
            return render_template('register.html', logged_in='user_id' in session.keys())
        db_hash = db_user.password_hash
        if pwd_hash != db_hash:
            return abort(406)
        else:
            session['user_id'] = db_user.user_id
            session['statut'] = db_user.statut
            return redirect('/')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        if request.form['re_password'] != password:
            return abort(400)
        else:
            hash = sha256()
            hash.update(password.encode('utf-8'))
            hashed_pwd = hash.hexdigest()
            db_user = User(password_hash=hashed_pwd, email=email, name=name, surname=surname, role='Citoyen', statut='User')
            db.session.add(db_user)
            db.session.commit()
            user_id = db_user.user_id
            session['user_id'] = user_id
            session['statut'] = 'User'
            return redirect('/')
    return render_template('register.html')


@app.route('/project/<article_id>')
def project(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    poster= Article.query.join(User, Article.poster_id==User.user_id).add_columns(User.name,User.surname).filter(article_id==Article.article_id).first()
    return render_template('article.html', article=article, poster=poster)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('statut', None)
    return redirect('/')

@app.route("/postpage", methods=['GET', 'POST'])
def publier():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['description']
        content = request.form['content']
        urlimg = request.form['imgurl']
        tag1=request.form['tag1']
        tag2=request.form['tag2']
        tag3=request.form['tag3']
        user_id=session.get('user_id')
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Il faut décrire votre projet')
        elif not desc:
            flash('Il faut décrire votre projet')
        else:
            post=Article(
                poster_id=user_id,
                title=title,
                img_link=urlimg,
                vote_pos=0,
                vote_neg=0,
                content=content, 
                description=desc, 
                post_time=datetime.now(), 
                deadline=datetime(2999, 12, 4), 
                tag1=tag1,
                tag2=tag2, 
                tag3=tag3)
            exists1 = db.session.query(Tags.tag_id).filter_by(tag_name=tag1).first() is not None
            exists2 = db.session.query(Tags.tag_id).filter_by(tag_name=tag2).first() is not None
            exists3 = db.session.query(Tags.tag_id).filter_by(tag_name=tag3).first() is not None
            if not exists1:
                newtag1=Tags(tag_name=tag1)
                db.session.add(newtag1) 
            if not exists2:
                newtag2=Tags(tag_name=tag2)
                db.session.add(newtag2)
            if not exists3:
                newtag3=Tags(tag_name=tag3)
                db.session.add(newtag3)
            db.session.add(post)
            db.session.commit()


    return render_template('postpage.html')

@app.route("/projects", methods = ['GET','POST'])
def listproject():
    articles = Article.query.all()
    tags=Tags.query.all()
    if request.method == "POST":
        tagsearched=request.form.get('mytag')
        results= Article.query.filter(or_(tagsearched==Article.tag1,tagsearched==Article.tag2,tagsearched==Article.tag3))
        return render_template('allprojects.html',articles=results, tags=tags)
    return render_template('allprojects.html',articles=articles, tags=tags,logged_in='user_id' in session.keys(), status=session.get('statut'))

@app.route("/profile", methods = ['GET'])
def pageprofil():
    return render_template('profile.html')
    