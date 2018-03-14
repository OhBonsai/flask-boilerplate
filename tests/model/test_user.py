# coding=utf-8
# Created by OhBonsai at 2018/3/14
from tests.data.users import sketch, create_group
from tests.data import add_fixture
from tests import check_db_object
from app.models.user import User, Group


def test_user_model(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    expected_result = frozenset([
        ('username', 'sketch'),
        ('email', 'letbonsaibe@gmail.com')
    ])

    check_db_object(expected_result, User)


def test_check_password(db_session):
    user, password = sketch()
    add_fixture(db_session, user)

    assert user.check_password(password)
    assert not user.check_password('invalid password')


def test_group_model(db_session):
    group = create_group()
    add_fixture(db_session, group)

    expected_result = frozenset([
        ('name', 'test')
    ])

    check_db_object(expected_result, Group)


def test_group_membership(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)

    group = create_group()
    user.groups.append(group)
    add_fixture(db_session, group)

    assert group in User.query.get(1).groups
