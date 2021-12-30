from flask import Flask, sessions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask import render_template, request, abort, url_for
from datetime import datetime
from hashlib import new, sha256

from sqlalchemy.sql.functions import current_timestamp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

db.create_all()

### insérer cette partie dans le code de app.py

def like_post(self):
    # prend le plus grand id existant pour créé un nouvel id non utilisé
    id = Vote.query(func.max(Vote.vote_id)) + 1

    # si pas déja voté on ajoute un vote direct
    if not self.has_voted():
        new_vote = Vote(vote_id=id, vote_on=Article.title(), parent_id=Article.article_id, user_id =self.user_id, user_vote=1, vote_time=datetime(current_timestamp()))
        Article.vote_pos += 1
        db.session.add(new_vote)
        db.session.commit()

    # si déja voté on récupère la valeur de vote total sur l'article et le contenue du vote
    else:
        val = Article.query.filter_by(Vote.parent_id == Article.article_id).first()
        val = val.vote_pos()
        val_vote = Vote.query.filter_by(Article.article_id == Vote.parent_id).first()
        val_vote = val.user_vote()

        # si le vote était négatif on modifie la bd et on change la date du vote
        if val_vote == -1:
            Vote.user_vote = 1
            Vote.vote_time = datetime(current_timestamp)
            Article.vote_pos += 1
            Article.vote_neg -= 1
            db.session.commit()

        # si le vote était positif on supprime le vote
        else:
            Vote.query.filter_by(user_id=self.user_id, parent_id=Article.article_id).delete()
            if val > 0:
                Article.vote_pos -= 1
            db.session.commit()



def dislike_post(self):
    # prend le plus grand id existant pour créé un nouvel id non utilisé
    id = Vote.query(func.max(Vote.vote_id)) + 1

    # si pas déja voté on ajoute un vote direct
    if not self.has_voted():
        new_vote = Vote(vote_id=id, vote_on=Article.title(), parent_id=Article.article_id, user_id =self.user_id, user_vote=-1, vote_time=datetime(current_timestamp()))
        Article.vote_neg += 1
        db.session.add(new_vote)
        db.session.commit()

    # si déja voté on récupère la valeur de vote total sur l'article et le contenue du vote
    else:
        val = Article.query.filter_by(Vote.parent_id == Article.article_id).first()
        val = val.vote_neg()
        val_vote = Vote.query.filter_by(Article.article_id == Vote.parent_id).first()
        val_vote = val.user_vote()

        # si le vote était positif on modifie la bd et on change la date du vote
        if val_vote == 1:
            Vote.user_vote = -1
            Vote.vote_time = datetime(current_timestamp)
            Article.vote_neg += 1
            Article.vote_pos -= 1
            db.session.commit()

        # si le vote était négatif on supprime le vote
        else:
            Vote.query.filter_by(user_id=self.user_id, parent_id=Article.article_id).delete()
            if val < 0:
                Article.vote_pos -= 1
            db.session.commit()



def has_voted(self):
    # répond True si il existe un vote avec l'id de l'utilisateur connecté et l'id de l'article
    return Vote.query.filter_by(
        Vote.user_id == self.user_id,
        Vote.parent_id == Article.article_id).count() > 0


#
# Reste maintenant à relié ces fonction au bouton correspondand
#