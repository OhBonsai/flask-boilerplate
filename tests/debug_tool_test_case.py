# coding=utf-8
# Created by OhBonsai at 2018/3/13
from tests.conftest import *
from tests.api.conftest import *

# what test_case i need debug
from tests.api.resource.test_post import test_request_all_my_posts
from tests.schema.schema.test_PostSchema import test_passed_deserialization_post_instance
from tests.model.test_patch import test_pass_add_comment


app = application()
for db in database(app):
    for ss in db_session(db, app):
        inner_app = application()
        for cc in client(inner_app):
            test_pass_add_comment(ss)
