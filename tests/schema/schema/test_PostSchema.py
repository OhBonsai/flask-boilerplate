# coding=utf-8
# Created by OhBonsai at 2018/3/14
import pytest

from marshmallow import ValidationError

from tests.data.posts import create_post
from tests.data.users import sketch
from tests.data import add_fixture
from app.schema.schema import PostSchema


def test_deserialization_fails_for_empty_title():
    with pytest.raises(ValidationError) as e:
        PostSchema(only=('title',)).load(dict(title=''))

    errors = e.value.messages
    assert 'title' in errors
    assert 'Must not be empty.' in errors.get('title')


def test_deserialization_fails_for_lack_title():
    with pytest.raises(ValidationError) as e:
        PostSchema().load(dict(sub='hello', content='Hello, I am Bonsai'))

    errors = e.value.messages
    print(errors)
    assert 1 == 1


def test_passed_serialization_request_json():
    data = PostSchema().load(dict(title='hello', sub='hello', content='Hello, I am Bonsai')).data
    assert data['title'] == 'hello'
    assert data['sub'] == 'hello'
    assert data['content'] == 'Hello, I am Bonsai'


def test_passed_deserialization_post_instance(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)

    post = create_post(user)
    add_fixture(db_session, post)

    data = PostSchema().dump(post).data

    assert data['id'] == post.id
    assert data['author'] == user.username
    assert data['title'] == post.title
    assert data['sub'] == post.sub
    assert data['content'] == post.content
    assert data['statuses'] == []
    assert data['comments'] == []
    assert data['tags'] == []


