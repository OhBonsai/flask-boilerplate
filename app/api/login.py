# coding=utf-8
# Created by OhBonsai at 2018/3/12
from flask_login import LoginManager, login_user, current_user
from app.models.user import User
from flask import request


class AnonymousUser(object):
    username = 'Anonymous'
    id = -1

    def __init__(self):
        pass

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError("Can't save AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Can't delete AnonymousUser.")

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_admin(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return

    def get_username(self):
        return self.username

    def __repr__(self):
        return self.username

login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    # if current_user and not current_user.is_anonymous:
    #     return current_user
    if request.authorization is not None and request.authorization.get('username') is not None:
        c_user = User.query.filter_by(username=request.authorization['username']).first()
        if c_user is not None and c_user.check_password(request.authorization['password']):
            login_user(c_user, remember=True)
            return c_user


@login_manager.request_loader
def load_user_from_request(request):
    # if current_user and not current_user.is_anonymous:
    #     return current_user
    if request.authorization is not None and request.authorization.get('username') is not None:
        c_user = User.query.filter_by(username=request.authorization['username']).first()
        if c_user.check_password(request.authorization['password']):
            login_user(c_user, remember=True)
            return c_user
