# coding=utf-8
# Created by OhBonsai at 2018/3/14
from tests.data.posts import create_post
from tests.data.users import sketch
from tests.data import add_fixture


def test_pass_add_tag(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)

    tag = post.Tag(user=user, tag='TEST')
    post.tags.append(tag)
    db_session.commit()

    assert tag.parent == post
    assert tag in post.tags
    assert tag.tag == 'TEST'


def test_pass_add_comment(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)

    comment = post.Comment(user=user, comment='TEST')
    post.comments.append(comment)
    db_session.commit()

    assert comment.parent == post
    assert comment in post.comments
    assert comment.comment == 'TEST'


def test_pass_set_status(db_session):
    user, _ = sketch()
    add_fixture(db_session, user)
    post = create_post(user)
    add_fixture(db_session, post)

    post.set_status('delete')
    status = post.statuses[0]

    assert status.parent == post
    assert status in post.statuses
    assert status.status == 'delete'


