# coding=utf-8
# Created by OhBonsai at 2018/3/7
from app.app import (
    create_app,
    create_http_app,
    create_api_app
)

from app.__about__ import (
    __title__,
    __summary__,
    __uri__,
    __version__,
    __author__,
    __email__,
    __license__
)
from app.models import db


application = create_app()


@application.teardown_appcontext
def shutdown_session(exception=None):
    """Remove the database session after every request or app shutdown"""
    db.session.remove()
