# coding=utf-8
# Created by OhBonsai at 2018/3/14
from tests.data.users import sketch, create_group
from tests.data.posts import create_post
from tests.data import add_fixture
from tests import check_db_object
from app.models.blog import Post


def test_post_model(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)

    expected_result = frozenset([
        ('title', post.title),
        ('sub', post.sub),
        ('user', user),
        ('content', post.content)
    ])
    check_db_object(expected_result, Post)
