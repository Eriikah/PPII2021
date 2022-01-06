from flask import Flask
from sqlalchemy.sql.expression import desc
from flask_sqlalchemy import SQLAlchemy
import app
from models import *
from hashlib import sha256
from app import *
app = Flask(__name__)
app.secret_key = '60a725867b515697115ccb2c561c2fee5694f2bc0d96372a4a033880702fa4a4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#def test_has_voted():
 #   has_voted=Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).count() > 0
  #  assert 
from models import *

def test_register():
    name = "jean"
    surname ="eude"
    email = "jean@eude.com"
    password = "password"

    hash = sha256()
    hash.update(password.encode('utf-8'))
    hashed_pwd = hash.hexdigest() 
    db_user = User(password_hash=hashed_pwd, email=email, name=name, surname=surname, role='Citoyen', statut='User')

def home(articles,pertinence_settings):
    art_ranking = {}
    for art in articles:
        art_score = 0
        for tag in [art.tag1, art.tag2, art.tag3]:
            score = pertinence_settings.get(tag)
            if score is not None:
                art_score += score
        art_ranking[art] = art_score
    return articles.sort(key=lambda a: art_ranking[a], reverse=True)
    
def articles():
    article1 = Article(article_id=1, poster_id=1, title='Premier Article', vote_pos=0, vote_neg=0, content='Contenu du premier article, lorem ipsum étou', description='ceci est un article', post_time=datetime(2021, 12, 4), deadline=datetime(2999, 12, 4), tag1='First', tag2 ='', tag3='', img_link='')
    article2 = Article(article_id=2, poster_id=1, title='Parlons Boissons', vote_pos=0, vote_neg=0, content='C\' est à boire c\'est à boire, c\'est à boire qu\'il nous faut.', description='Ouverture taverne place du marché', post_time=datetime(2024, 7, 18), deadline=datetime(2999, 12, 4), tag1='Boire', tag2 ='Taverne', tag3='Marché', img_link='')
    article3 = Article(article_id=3, poster_id=4, title='Votre maire est arrivé sur la plateforme', vote_pos=0, vote_neg=0, content='Salut Monsieur le maire', description='Accueillons ensemble notre maire bien aimé', post_time=datetime(2021, 12, 7), deadline=datetime(2999, 12, 4), tag1='Maire', tag2 ='Premier', tag3='', img_link='')
    article4 = Article(article_id=4, poster_id=4, title='Nouveau parc pour enfants', vote_pos=0, vote_neg=0, content='Vive les enfants (non)', description='Un nouveau parc ouvre ses portes près de la place Gagarine', post_time=datetime(2023, 8, 25), deadline=datetime(2999, 12, 4), tag1='Parc', tag2 ='Ouverture', tag3='Gagarine', img_link='')
    article5 = Article(article_id=5, poster_id=2, title='Extension autoroute', vote_pos=0, vote_neg=0, content='Vroum Vroum!', description='Luttons contre une urbanisation démesurée. Rendez-vous devant la mairie jeudi 16 décembre pour manifester', post_time=datetime(2021, 12, 8), deadline=datetime(2021, 12, 17), tag1='Autoroute', tag2 ='Mairie', tag3='Manifestation', img_link='')
    articles = [article1,article2,article3,article4,article5]
    pertinence_settings = {1: {'First': -3, 'Boire': 4, 'Taverne':0, 'Parc':3, 'Maire':-3}}
    res= home(articles,pertinence_settings)
    assert res[1]==article3    
    assert res[0]==article2
    pertinence_settings={1: {'First': 3, 'Boire': 0, 'Taverne':-2, 'Parc':3, 'Maire':4}}
    res2=home(articles,pertinence_settings)
    assert res2[0]==article3
    assert res2[1]==article1
    assert res2[2]==article3
  