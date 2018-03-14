# coding=utf-8
# Created by OhBonsai at 2018/3/14

from app.schema.schema import CommentSchema

from tests.data.users import sketch
from tests.data import add_fixture
from tests.data.posts import create_post
# CommentSchema Won't been used in Deserialization


def test_passes_for_dump_comment_instance(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)

    comment = post.Comment(user=user, comment="哈哈， 我来评论啦")
    data = CommentSchema().dump(comment).data

    assert data['author'] == 'sketch'
    assert data['comment'] == '哈哈， 我来评论啦'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
