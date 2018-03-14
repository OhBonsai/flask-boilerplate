# coding=utf-8
# Created by OhBonsai at 2018/3/13
from app.models import Post
from faker import Faker
from tests.data.users import sketch


def create_posts(user, n=50):
    fake = Faker()
    fake.seed(32)

    posts = []
    for i in range(n):
        p = Post(
            title=fake.name(),
            sub=fake.address(),
            user=user,
            content=fake.text()
        )
        posts.append(p)
    return posts


def create_post(user):
    fake = Faker()
    fake.seed(32)

    return Post(
        title=fake.name(),
        sub=fake.address(),
        user=user,
        content=fake.text()
    )
