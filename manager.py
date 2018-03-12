# coding=utf-8
# Created by OhBonsai at 2018/3/12

"""This module is for management of the application."""


import sys

from flask_migrate import MigrateCommand
from flask_script import Command
from flask_script import Manager
from flask_script import Server
from flask_script import Option
from flask_script import prompt_bool
from flask_script import prompt_pass

from sqlalchemy.exc import IntegrityError

from app import create_api_app
from app.models import db_session
from app.models import drop_all
from app.models.user import Group
from app.models.user import User


class DropDataBaseTables(Command):
    """Drop all database tables."""

    def __init__(self):
        super(DropDataBaseTables, self).__init__()

    def run(self):
        """Drop all tables after user ha verified."""

        verified = prompt_bool(
            'Do you really want to drop all the database tables?')
        if verified:
            sys.stdout.write('All tables dropped. Database is now empty.\n')
            drop_all()


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
        db_session.add(user)
        db_session.commit()
        sys.stdout.write('User {0:s} created/updated\n'.format(username))


class AddGroup(Command):
    """Create a new app group."""

    option_list = (Option('--name', '-n', dest='name', required=True), )

    def __init__(self):
        super(AddGroup, self).__init__()

    def run(self, name):
        """Creates the group."""
        group = Group.get_or_create(name=name)
        db_session.add(group)
        db_session.commit()
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
                db_session.commit()
            except ValueError:
                sys.stdout.write('{0:s} is not a member of group {1:s}\n'.
                                 format(user_name, group_name))
        else:
            user.groups.append(group)
            try:
                db_session.commit()
                sys.stdout.write('{0:s} added to group {1:s}\n'.format(
                    user_name, group_name))
            except IntegrityError:
                sys.stdout.write('{0:s} is already a member of group {1:s}\n'.
                                 format(user_name, group_name))


if __name__ == '__main__':
    shell_manager = Manager(create_api_app)
    shell_manager.add_command('add_user', AddUser())
    shell_manager.add_command('add_group', AddGroup())
    shell_manager.add_command('manage_group', GroupManager())
    shell_manager.add_command('db', MigrateCommand)
    shell_manager.add_command('drop_db', DropDataBaseTables())
    shell_manager.add_command('runserver', Server(host='127.0.0.1', port=5000))
    shell_manager.add_option(
        '-c',
        '--config',
        dest='config_file',
        # default='./config/default.conf.py',
        required=False)
    shell_manager.run()
