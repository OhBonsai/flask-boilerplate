# coding=utf-8
# Created by OhBonsai at 2018/3/14
import pytest
from marshmallow import ValidationError

from app.schema.plus import String, Schema, NotEmpty


class SampleSchema(Schema):
    name = String(validate=NotEmpty())


def test_fails_for_empty_string():
    with pytest.raises(ValidationError) as e:
        SampleSchema().load(dict(name=''))

    errors = e.value.messages
    assert 'name' in errors
    assert 'Must not be empty.' in errors['name']


def test_passes_for_non_empty_string():
    data = SampleSchema().load(dict(name='foobar')).data
    assert data['name'] == 'foobar'


def test_passes_for_blank_string():
    data = SampleSchema().load(dict(name='    ')).data
    assert data['name'] == '    '


def test_fails_for_stripped_blank_string():
    class TestSchema2(Schema):
        name = String(strip=True, validate=NotEmpty())

    with pytest.raises(ValidationError) as e:
        TestSchema2().load(dict(name='    '))

    errors = e.value.messages
    assert 'name' in errors
    assert 'Must not be empty.' in errors['name']
