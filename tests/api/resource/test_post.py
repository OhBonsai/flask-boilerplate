# coding=utf-8
# Created by OhBonsai at 2018/3/13
from tests.data import add_fixture, add_fixtures, posts, users


def test_request_all_my_posts(db_session, client):
    user, pwd = users.sketch()
    add_fixture(db_session, user)
    post_instances = posts.create_posts(user, 10)
    add_fixtures(db_session, *post_instances)

    res = client.get('/api/v1/posts', user=user, password=pwd)
    assert res.status_code == 200
