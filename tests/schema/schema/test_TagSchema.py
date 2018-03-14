# coding=utf-8
# Created by OhBonsai at 2018/3/14

from app.schema.schema import TagSchema

from tests.data.users import sketch
from tests.data import add_fixture
from tests.data.posts import create_post


# Tag Won't been used in Deserialization
def test_passes_for_dump_tag_instance(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)

    tag = post.Tag(user=user, tag="CMDB")
    data = TagSchema().dump(tag).data

    assert data['author'] == 'sketch'
    assert data['tag'] == 'CMDB'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
