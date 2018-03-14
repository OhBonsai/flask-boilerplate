# coding=utf-8
# Created by OhBonsai at 2018/3/14
from app.schema.plus import String, Schema


def test_default_deserialization():
    class TestSchema(Schema):
        name = String()

    data, errors = TestSchema().load(dict(name='   foo bar   '))
    assert not errors
    assert data.get('name') == '   foo bar   '


def test_stripping_deserialization():
    class TestSchema(Schema):
        name = String(strip=True)

    data, errors = TestSchema().load(dict(name='   foo bar   '))
    assert not errors
    assert data.get('name') == 'foo bar'
