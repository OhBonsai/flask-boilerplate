# coding=utf-8
# Created by OhBonsai at 2018/3/13
from tests.conftest import *
from tests.api.conftest import *

# what test_case i need debug
from tests.api.resource.post_test import test_request_all_my_posts


app = application()
for db in database(app):
    for ss in db_session(db, app):
        inner_app = application()
        for cc in client(inner_app):
            test_request_all_my_posts(ss, cc)
