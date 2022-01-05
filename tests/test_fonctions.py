import app
import pytest
from models import *



def test_has_voted():
    articles=Article.query.all()
    users=User.query.all()
    for article in articles:
        for self in users:
            has_voted=Vote.query.filter_by(user_id=self.user_id, parent_id=article.article_id).count() > 0
            assert type(has_voted)==bool

