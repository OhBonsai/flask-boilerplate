# coding=utf-8
# Created by OhBonsai at 2018/3/13
"""This module is for management of the application."""

from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from app import create_api_app
from app.command.database import manager as db_manager
from app.command.user import AddUser, AddGroup, GroupManager


shell_manager = Manager(create_api_app)
shell_manager.add_command('add_user', AddUser())
shell_manager.add_command('add_group', AddGroup())
shell_manager.add_command('manage_group', GroupManager())
shell_manager.add_command('db', db_manager)
shell_manager.add_command('migrate', MigrateCommand)
shell_manager.add_command('runserver', Server(host='127.0.0.1', port=8001))
shell_manager.add_option(
    '-c',
    '--config',
    dest='config_file',
    default=None,
    required=False)

