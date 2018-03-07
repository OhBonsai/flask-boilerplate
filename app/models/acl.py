# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""Three permissions in ACL system: "read", "write" and "delete".
Two role relate with permission : "user", "group"
"""

from flask_login import current_user
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    and_,
    or_,
    not_
)
from sqlalchemy.types import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.models import (
    BaseModel,
    db_session
)


class AccessControlEntry(object):
    """ACL model.
    """

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey('user.id'))

    @declared_attr
    def user(self):
        return relationship('User')

    @declared_attr
    def group_id(self):
        return Column(Integer, ForeignKey('group.id'))

    @declared_attr
    def group(self):
        return relationship('Group')

    # Permission (read, write, delete)
    permission = Column(String(16))


class AccessControlMixin(object):
    """Model use this mixin will generate some tables to make permission enable
    """

    @declared_attr
    def acl(self):
        """
        Generates the ACE Model and add ace field to parent model
        """

        self.AccessControlEntry = type(
            '{}sAccessControlEntry'.format(self.__name__),
            (AccessControlEntry, BaseModel),
            dict(
                __tablename__='{}_ace'.format(self.__tablename__),
                parent_id=Column(Integer, ForeignKey('{}.id'.format(self.__tablename__))),
                parent=relationship(self)
            )
        )
        return relationship(self.AccessControlEntry)

    @classmethod
    def all_with_acl(cls, user=None):
        """Get all instances that the user has read permission on.

        :param user: User instance
        :return: instance of app.models.AclBaseQuery
        """

        if not user:
            user = current_user

        return cls.query.filter(
            or_(cls.AccessControlEntry.user == user,
                and_(cls.AccessControlEntry.user == None,
                     cls.AccessControlEntry.group == None),
                cls.AccessControlEntry.group_id.in_([
                    group.id for group in user.groups
                ])), cls.AccessControlEntry.permission == u'read',
            cls.AccessControlEntry.parent)


    def _get_ace(self, permission, user=None, group=None, check_group=True):
        """Get the specific access control entry for the user and permission.

        :param permission: String (read, write, delete)
        :param user: app.models.user.User instance
        :param group: app.models.user.Group instance
        :param check_group: Does check group permission, default is True
        :return: An Access control entry or None
        """

        # Check group firstly.
        if group:
            return self.AccessControlEntry.query.filter_by(
                group=group, permission=permission, parent=self).all()

        aces = self.AccessControlEntry.query.filter_by(
            user=user, group=None, permission=permission, parent=self).all()

        if (user and check_group) and not aces:
            group_intersection = set(user.groups) & set(self.groups)
            for _group in group_intersection:
                aces = self.AccessControlEntry.query.filter_by(
                    group=_group, permission=permission, parent=self).all()
                if aces:
                    return aces
        return aces

    @property
    def groups(self):
        """List what group have permission to this model.

        :return: set of groups
        """

        group_aces = self.AccessControlEntry.query.filter(
            not_(self.AccessControlEntry.group == None),
            self.AccessControlEntry.parent == self).all()
        return set(ace.group for ace in group_aces)

    @property
    def is_public(self):
        """Determine if this instance is open to everyone.

        :return: an ace if the object is readable by everyone OR None
        """
        return self._get_ace(permission='read', user=None, group=None)

    @property
    def friends(self):
        """Get list of users that have explicit read permission on this instance

        :return: List of users
        """
        aces = self.AccessControlEntry.query.filter(
            not_(self.AccessControlEntry.user == self.user),
            not_(self.AccessControlEntry.user == None),
            self.AccessControlEntry.permission == 'read',
            self.AccessControlEntry.parent == self
        ).all()
        return set(ace.user for ace in aces)

    def has_permission(self, user, permission):
        """
        :param user:  User instance
        :param permission: (read, write, delete)
        :return: ace if user has permission or None
        """
        public_ace = self.is_public
        if public_ace and permission == 'read':
            return public_ace
        return self._get_ace(permission=permission, user=user)

    def grant_permission(self, permission, user=None, group=None):
        """ Grant permission to a user or group

        :param permission: (read, write, delete)
        :param user: User instance
        :param group: Group instance
        """
        if group and not self._get_ace(permission, group=group):
            self.acl.append(self.AccessControlEntry(permission=permission, group=group))
            db_session.commit()
            return

        if not self._get_ace(permission, user=user, check_group=False):
            self.acl.append(self.AccessControlEntry(permission=permission, user=user))
            db_session.commit()

    def revoke_permission(self, permission, user=None, group=None):
        """Revoke permission for user/group.

        :param permission: (read, write, delete)
        :param user: User instance
        :param group: Group instance
        """

        if group:
            group_ace = self._get_ace(permission=permission, group=group)
            if group_ace:
                for ace in group_ace:
                    self.acl.remove(ace)
                db_session.commit()
            return

        user_ace = self._get_ace(permission=permission, user=user)
        if user_ace:
            for ace in user_ace:
                self.acl.remove(ace)
            db_session.commit()
