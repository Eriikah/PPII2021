from app import db
from models import *
from datetime import datetime
from hashlib import sha256

hash = sha256()

article1 = Article(article_id=1, poster_id=1, title='Premier Article', vote_pos=0, vote_neg=0, content='Contenu du premier article, lorem ipsum étou', description='ceci est un article', post_time=datetime(2021, 12, 4), deadline=datetime(2999, 12, 4), tag1='First', tag2 ='', tag3='', img_link='')
article2 = Article(article_id=2, poster_id=1, title='Parlons Boissons', vote_pos=0, vote_neg=0, content='C\' est à boire c\{est à boire, c\'est à boire qu\'il nous faut.', description='Ouverture taverne place du marché', post_time=datetime(2024, 7, 18), deadline=datetime(2999, 12, 4), tag1='Boire', tag2 ='Taverne', tag3='Marché', img_link='')
article3 = Article(article_id=3, poster_id=4, title='Votre maire est arrivé sur la plateforme', vote_pos=0, vote_neg=0, content='Salut Monsieur le maire', description='Accueillons ensemble notre maire bien aimé', post_time=datetime(2021, 12, 7), deadline=datetime(2999, 12, 4), tag1='Maire', tag2 ='Premier', tag3='', img_link='')
article4 = Article(article_id=4, poster_id=4, title='Nouveau parc pour enfants', vote_pos=0, vote_neg=0, content='Vive les enfants (non)', description='Un nouveau parc ouvre ses portes près de la place Gagarine', post_time=datetime(2023, 8, 25), deadline=datetime(2999, 12, 4), tag1='Parc', tag2 ='Ouverture', tag3='Gagarine', img_link='')
article5 = Article(article_id=5, poster_id=2, title='Extension autoroute', vote_pos=0, vote_neg=0, content='Vroum Vroum!', description='Luttons contre une urbanisation démesurée. Rendez-vous devant la mairie jeudi 16 décembre pour manifester', post_time=datetime(2021, 12, 8), deadline=datetime(2021, 12, 17), tag1='Autoroute', tag2 ='Mairie', tag3='Manifestation', img_link='')

h1 = sha256()
h1.update('motdepasse'.encode('utf-8'))
mdp1 = h1.hexdigest()
user1 = User(user_id='1',password_hash=mdp1,email='JeanEude@gmail.com',name='Jean',surname='Eude',role='Admin',statut='Admin')
h2 = sha256()
h2.update('password123'.encode('utf-8'))
mdp2 = h2.hexdigest()
user2 = User(user_id='2',password_hash=mdp2,email='Manifestant.Beton@gmail.com',name='Franck',surname='Iste',role='Syndicat',statut='Poster')
h3 = sha256()
h3.update('123456'.encode('utf-8'))
mdp3 = h3.hexdigest()
user3 = User(user_id='3',password_hash=mdp3,email='MadameLambda@gmail.com',name='Lora',surname='Tonlaveure',role='Citoyen',statut='User')
h4 = sha256()
h4.update('mot_de_passe'.encode('utf-8'))
mdp4 = h4.hexdigest()
user4 = User(user_id='4',password_hash=mdp4,email='AdjointMaire.Gouvigny@gmail.com',name='Hédemé',surname='Mouar',role='Adjoint',statut='Poster')

t1=Tags(tag_id=1,tag_name="First")
t2=Tags(tag_id=2,tag_name="Boire")
t3=Tags(tag_id=3,tag_name="Mairie")
t4=Tags(tag_id=4,tag_name="Maire")
t5=Tags(tag_id=5,tag_name="Taverne")
t6=Tags(tag_id=6,tag_name="Marché")
t7=Tags(tag_id=7,tag_name="Parc")
t8=Tags(tag_id=8,tag_name="Ouverture")
t8=Tags(tag_id=8,tag_name="Gargarine")
t9=Tags(tag_id=9,tag_name="Autoroute")
t10=Tags(tag_id=10,tag_name="Manifestation")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(article1)
db.session.add(article2)
db.session.add(article3)
db.session.add(article4)
db.session.add(article5)
db.session.add(t1)
db.session.add(t2)
db.session.add(t3)
db.session.add(t4)
db.session.add(t5)
db.session.add(t6)
db.session.add(t7)
db.session.add(t8)
db.session.add(t9)
db.session.add(t10)
db.session.commit()