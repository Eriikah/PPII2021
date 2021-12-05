from app import db
from models import *
from datetime import date

article1 = Article(article_id='1', poster_id='1', title='Premier Article', vote_pos='0', vote_neg='0', content='', description='ceci est un article', post_time='date(2021, 12, 4)', deadline='date(2999, 12, 4)', tag1='First', tag2 ='', tag3='')
article2 = Article(article_id='2', poster_id='1', title='Parlons Boissons', vote_pos='0', vote_neg='0', content='', description='Ouverture taverne place du marché', post_time='date(2024, 7, 18)', deadline='date(2999, 12, 4)', tag1='Boire', tag2 ='Taverne', tag3='Marché')
article3 = Article(article_id='3', poster_id='4', title='Votre maire est arrivé sur la plateforme', vote_pos='0', vote_neg='0', content='', description='Accueillons ensemble notre maire bien aimé', post_time='date(2021, 12, 7)', deadline='date(2999, 12, 4)', tag1='Maire', tag2 ='Premier', tag3='')
article4 = Article(article_id='4', poster_id='4', title='Nouveau parc pour enfants', vote_pos='0', vote_neg='0', content='', description='Un nouveau parc ouvre ses portes près de la place Gagarine', post_time='date(2023, 8, 25)', deadline='date(2999, 12, 4)', tag1='Parc', tag2 ='Ouverture', tag3='Gagarine')
article5 = Article(article_id='5', poster_id='2', title='Extension autoroute', vote_pos='0', vote_neg='0', content='', description='Luttons contre une urbanisation démesurée. Rendez-vous devant la mairie jeudi 16 décembre pour manifester', post_time='date(2021, 12, 8)', deadline='date(2021, 12, 17)', tag1='Autoroute', tag2 ='Mairie', tag3='Manifestation')

user1 = User(user_id='1',password_hash='',email='JeanEude@gmail.com',name='Jean',surname='Eude',role='Admin',statut='Admin')
user2 = User(user_id='2',password_hash='',email='Manifestant.Beton@gmail.com',name='Franck',surname='Iste',role='Syndicat',statut='Poster')
user3 = User(user_id='3',password_hash='',email='MadameLambda@gmail.com',name='Lora',surname='Tonlaveure',role='Citoyen',statut='User')
user4 = User(user_id='4',password_hash='',email='AdjointMaire.Gouvigny@gmail.com',name='Hédemé',surname='Mouar',role='Adjoint',statut='Poster')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(article1)
db.session.add(article2)
db.session.add(article3)
db.session.add(article4)
db.session.add(article5)
db.session.commit()