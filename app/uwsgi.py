# coding=utf-8
# Created by OhBonsai at 2018/3/16
from app.app import create_api_app
from app.models import db


application = create_api_app(config_file='/etc/sketch.conf')


@application.teardown_appcontext
def shutdown_session(exception=None):
    """Remove the database session after every request or app shutdown"""
    db.session.remove()
