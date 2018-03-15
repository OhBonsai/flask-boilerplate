# coding=utf-8
# Created by OhBonsai at 2018/3/9
from .local import LocalConfig
from .test import TestConfig


config = {
    "local": LocalConfig,
    "test": TestConfig
}
