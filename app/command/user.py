# coding=utf-8
# Created by OhBonsai at 2018/3/13
import sys

from flask_script import Command, Option, prompt_pass
from sqlalchemy.exc import IntegrityError

from app.models import db, Group, User


class AddUser(Command):
    """Create a new app user."""

    option_list = (
        Option('--username', '-', dest='username', required=True),
        Option('--password', '-p', dest='password', required=False), )

    def __init__(self):
        super(AddUser, self).__init__()

    def get_password_from_prompt(self):
        """Get password from the command line prompt."""

        first_password = prompt_pass('Enter password')
        second_password = prompt_pass('Enter password again')
        if first_password != second_password:
            sys.stderr.write('Passwords don\'t match, try again.\n')
            self.get_password_from_prompt()
        return first_password

    def run(self, username, password):
        """Creates the user."""
        if not password:
            password = self.get_password_from_prompt()
        user = User.get_or_create(username=username)
        user.set_password(plaintext=password)
        db.session.add(user)
        db.session.commit()
        sys.stdout.write('User {0:s} created/updated\n'.format(username))


class AddGroup(Command):
    """Create a new app group."""

    option_list = (Option('--name', '-n', dest='name', required=True), )

    def __init__(self):
        super(AddGroup, self).__init__()

    def run(self, name):
        """Creates the group."""
        group = Group.get_or_create(name=name)
        db.session.add(group)
        db.session.commit()
        sys.stdout.write('Group {0:s} created\n'.format(name))


class GroupManager(Command):
    """Manage group memberships."""

    option_list = (
        Option(
            '--add',
            '-a',
            dest='add',
            action='store_true',
            required=False,
            default=False),
        Option(
            '--remove',
            '-r',
            dest='remove',
            action='store_true',
            required=False,
            default=False),
        Option('--group', '-g', dest='group_name', required=True),
        Option('--user', '-', dest='user_name', required=True), )

    def __init__(self):
        super(GroupManager, self).__init__()

    def run(self, add, remove, group_name, user_name):
        """Add the user to the group."""

        group = Group.query.filter_by(name=group_name).first()
        user = User.query.filter_by(username=user_name).first()

        # Add or remove user from group
        if remove:
            try:
                user.groups.remove(group)
                sys.stdout.write('{0:s} removed from group {1:s}\n'.format(
                    user_name, group_name))
                db.session.commit()
            except ValueError:
                sys.stdout.write('{0:s} is not a member of group {1:s}\n'.
                                 format(user_name, group_name))
        else:
            user.groups.append(group)
            try:
                db.session.commit()
                sys.stdout.write('{0:s} added to group {1:s}\n'.format(
                    user_name, group_name))
            except IntegrityError:
                sys.stdout.write('{0:s} is already a member of group {1:s}\n'.
                                 format(user_name, group_name))
