from flask import Flask
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, abort, url_for, session, redirect
from hashlib import sha256
from datetime import datetime
from sqlalchemy import or_
import pickle

from sqlalchemy.orm import query
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import func


app = Flask(__name__)
app.secret_key = '60a725867b515697115ccb2c561c2fee5694f2bc0d96372a4a033880702fa4a4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

db.create_all()

def like_post(self,article):
    # prend le plus grand id existant pour créé un nouvel id non utilisé
    idmax = db.session.query(func.max(Vote.vote_id)).scalar()
    if idmax == None:
        id = 1
    else:
        id = idmax + 1

    # si pas déja voté on ajoute un vote direct
    if not has_voted(self,article):
        new_vote = Vote(vote_id=id, vote_on=article.title, parent_id=article.article_id, user_id =self.user_id, user_vote=1, vote_time=current_timestamp())
        article.vote_pos += 1
        db.session.add(new_vote)
        db.session.commit()

    # si déja voté on récupère la valeur de vote total sur l'article et le contenue du vote
    else:
        val = article.vote_pos
        vote = Vote.query.filter(article.article_id == Vote.parent_id).first()
        val_vote = vote.user_vote

        # si le vote était négatif on modifie la bd et on change la date du vote
        if val_vote == -1:
            vote.user_vote = 1
            vote.vote_time = current_timestamp()
            article.vote_pos += 1
            article.vote_neg -= 1
            db.session.commit()

        # si le vote était positif on supprime le vote
        else:
            Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).delete()
            article.vote_pos -= 1
            db.session.commit()



def dislike_post(self,article):
    # prend le plus grand id existant pour créé un nouvel id non utilisé
    idmax = db.session.query(func.max(Vote.vote_id)).scalar()
    if idmax == None:
        id = 1
    else:
        id = idmax + 1

    # si pas déja voté on ajoute un vote direct
    if not has_voted(self,article):
        new_vote = Vote(vote_id=id, vote_on=article.title, parent_id=article.article_id, user_id =self.user_id, user_vote=-1, vote_time=current_timestamp())
        article.vote_neg += 1
        db.session.add(new_vote)
        db.session.commit()

    # si déja voté on récupère la valeur de vote total sur l'article et le contenue du vote
    else:
        val = article.vote_neg
        vote = Vote.query.filter(article.article_id == Vote.parent_id).first()
        val_vote = vote.user_vote

        # si le vote était positif on modifie la bd et on change la date du vote
        if val_vote == 1:
            vote.user_vote = -1
            vote.vote_time = current_timestamp()
            article.vote_neg += 1
            article.vote_pos -= 1
            db.session.commit()

        # si le vote était négatif on supprime le vote
        else:
            Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).delete()
            article.vote_neg -= 1
            db.session.commit()



def has_voted(self,article):
    # répond True si il existe un vote avec l'id de l'utilisateur connecté et l'id de l'article
    return Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).count() > 0

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
        if not email or not pwd or not email and pwd:
            flash("Field requiered")
            return redirect("/login")
        h.update(pwd.encode('utf-8'))
        pwd_hash = h.hexdigest()
        db_user = User.query.filter_by(email=email).first()
        if db_user is None:
            flash("Email non reconnu, êtes vous sûr de l'orthographe?")
            return redirect("/login")
        db_hash = db_user.password_hash
        if pwd_hash != db_hash:
            flash("Mot de passe non reconnu, êtes vous sûr de l'orthographe?")
            return redirect("/login")
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
    vote = Vote.query.filter(article.article_id == Vote.parent_id).first()
    return render_template('article.html', article=article, poster=poster, vote=vote)


@app.route('/project/like/<article_id>')
def like_article(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    user = User.query.filter(User.user_id==session.get('user_id')).first()
    like_post(user,article)
    return redirect('/project/' + article_id)

@app.route('/project/dislike/<article_id>')
def dislike_article(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    user = User.query.filter(User.user_id==session.get('user_id')).first()
    dislike_post(user,article)
    return redirect('/project/' + article_id)

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
        tag1=request.form['tag1']
        tag2=request.form['tag2']
        tag3=request.form['tag3']
        user_id=session.get('user_id')
        if request.files:
            file = request.files['file']
        if not file:
            flash('Il faut illustrez votre projet')
        else:
            uid=""
            if request.files:
                filename, ext = file.filename.rsplit('.', 1)
                ext = ext.lower()
                hash = sha256()
                hash.update(file.read(-1))
                uid = hash.hexdigest()
                file.stream.seek(0)
                file.save(f'static/'+ uid +'.'+ext)  
            post=Article(
                poster_id=user_id,
                title=title,
                img_link=uid +'.'+ext,
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
            return redirect("/projects")

    return render_template('postpage.html')


@app.route("/projects", methods = ['GET','POST'])
def listproject():
    articles = Article.query.all()
    tags=Tags.query.all()
    if request.method == "POST":
        tagsearched=request.form.get('mytag')
        results= Article.query.filter(or_(tagsearched==Article.tag1,tagsearched==Article.tag2,tagsearched==Article.tag3))
        return render_template('allprojects.html',articles=results, tags=tags)
    return render_template('allprojects.html',articles=articles, tags=tags, logged_in='user_id' in session.keys(), status=session.get('statut'))

@app.route("/profile", methods = ['GET','POST'])
def pageprofil():
    if session.get('user_id') is None:
        return render_template('profile.html',user=None)
    user = User.query.filter(User.user_id==session.get('user_id')).first()
    if request.method == "POST":
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.password = request.form['password']
        if request.form['re_password'] != user.password:
            return abort(400)
        else:
            hash = sha256()
            hash.update(user.password.encode('utf-8'))
            hashed_pwd = hash.hexdigest()
            db.session.commit()
        return redirect("/")
    
    return render_template('profile.html' , user=user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_terms = request.args.get('search')
    curr_user_id = session.get('user_id')
    if curr_user_id is not None:
        user_cookies = None
        with open('pertinence_cookies', 'rb') as pc:
            pertinence_cookies = pickle.load(pc)
            user_cookies = pertinence_cookies.get(curr_user_id) or {} # sets the cookies to an empty dict if they are None
        for term in search_terms.split():
            if term not in user_cookies.keys():
                user_cookies[term] = 1
            else:
                user_cookies[term] += 1
        pertinence_cookies[curr_user_id] = user_cookies
        with open('pertinence_cookies', 'wb') as pc:
            pickle.dump(pertinence_cookies, pc)
    terms=search_terms.split() 
    filter=[(or_(Article.tag1.contains(term),Article.tag2.contains(term),Article.tag3.contains(term),Article.title.contains(term),Article.content.contains(term),Article.description.contains(term))) for term in terms]
    query=Article.query.filter(or_(*filter))
    results=query.all()
    if query.count()==0:
       flash('No results found')
       return redirect('/noresult')
    tags=Tags.query.all()                
    if request.method == "POST":
        tagsearched=request.form.get('mytag')
        results= Article.query.filter(or_(tagsearched==Article.tag1,tagsearched==Article.tag2,tagsearched==Article.tag3))
        return render_template('allprojects.html',articles=results, tags=tags)
    return render_template('allprojects.html',articles=results, tags=tags)

@app.route('/noresult')
def noresult():
    return render_template('noresult.html',logged_in='user_id' in session.keys(), status=session.get('statut'))
