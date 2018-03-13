# coding=utf-8
# Created by OhBonsai at 2018/3/13
from tests.data import add_fixture, add_fixtures, posts, users


def test_request_all_my_posts(db_session, client):
    sketch, pwd = users.sketch()
    add_fixture(db_session, sketch)
    post_instances = posts.test_posts(sketch, 10)
    add_fixtures(db_session, *post_instances)

    res = client.get('/api/v1/posts', user=sketch, password=pwd)
    assert res.status_code == 200
