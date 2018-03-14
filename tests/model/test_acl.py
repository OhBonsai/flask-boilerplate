# coding=utf-8
# Created by OhBonsai at 2018/3/14

from tests.data.posts import create_post
from tests.data.users import sketch, create_group
from tests.data import add_fixture


def test_passes_change_permission(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)
    group = create_group()
    # update user data
    user.groups.append(group)
    add_fixture(db_session, group)

    for permission in ('read', 'write', 'delete'):
        assert not post.has_permission(permission=permission, user=user)

        post.grant_permission(permission=permission, group=group)
        # user in group
        assert post.has_permission(permission=permission, user=user)
        post.revoke_permission(permission=permission, group=group)
        assert not post.has_permission(permission=permission, user=user)


def test_passes_change_instance_public(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)

    post.grant_permission(permission='read')
    assert post.is_public
    post.revoke_permission(permission='read')
    assert not post.is_public
