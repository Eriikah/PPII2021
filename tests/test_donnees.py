from datetime import date, datetime
import pytest
from models import *

db.create_all()


def test_donnees():
    users,articles,tags,votes=User.query.all(),Article.query.all(),Tags.query.all(),Vote.query.all()

    for user in users:
        assert type(user.name)==str
        assert type(user.user_id)==int
        assert type(user.password_hash)==str
        assert type(user.email)==str
        assert type(user.surname)==str
        assert type(user.role)==str
        assert type(user.statut)==str

    for article in articles:
        assert type(article.article_id)==int
        assert type(article.poster_id)==int
        assert type(article.title)==str
        assert type(article.img_link)==str
        assert type(article.vote_pos)==int
        assert type(article.vote_neg)==int
        assert type(article.content)==str
        assert type(article.description)==str
        assert type(article.post_time)==datetime
        assert type(article.deadline)==datetime
        assert type(article.tag1)==str
        assert type(article.tag2)==str
        assert type(article.tag3)==str

    for tag in tags:
        assert type(tag.tag_id)==int
        assert type(tag.tag_name)==str
    
    for vote in votes:
        assert type(vote.vote_id)==int
        assert type(vote.parent_id)==int
        assert type(vote.parent_id)==int
        assert type(vote.user_id)==int
        assert type(vote.user_vote)==int
        assert type(vote.vote_time)==datetime

