# coding=utf-8
# Created by OhBonsai at 2018/3/14


from app.schema.schema import StatusSchema

from tests.data.users import sketch
from tests.data import add_fixture
from tests.data.posts import create_post
# Status Won't been used in Deserialization


def test_passes_for_dump_status_instance(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)

    status = post.Status(user=user, status="delete")
    data = StatusSchema().dump(status).data

    assert data['author'] == 'sketch'
    assert data['status'] == 'delete'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
