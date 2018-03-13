# coding=utf-8
# Created by OhBonsai at 2018/3/13
from tests.data import add_fixtures, posts


def test_request_all_my_posts(db_session, client):
    post_instances = posts.test_posts(10)
    add_fixtures(db_session, post_instances)

    res = client.get('/api/v1/posts')
    assert res.status_code == 200
