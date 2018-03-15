# coding=utf-8
# Created by OhBonsai at 2018/3/15
import re
import os


SETTING_PATTERN = re.compile(r'[A-Z_0-9]*')


class NeedUpperCharError(Exception):
    pass


class ConfigRestrictMeta(type):
    def __new__(cls, name, bases, dct):
        for key in dct:
            if not key.startswith('__'):
                if SETTING_PATTERN.fullmatch(key) is None:
                    raise NeedUpperCharError("Setting must match [A-Z_0-9]*. [{}] is unleggal".format(key))

                # Env setting priority
                dct[key] = os.getenv('APP_'+key, dct[key])
        return type.__new__(cls, name, bases, dct)

