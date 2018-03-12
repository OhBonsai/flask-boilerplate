# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""Define some subclass base on mashmallow"""

from marshmallow import Schema as _Schema
from marshmallow.fields import String as _String
from marshmallow.validate import Validator, ValidationError


class String(_String):
    """Sub class of mashmallow.fields.String, make string value strip"""

    def __init__(self, strip=False, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)
        self.strip = strip

    def _deserialize(self, value, attr, data):
        value = super(String, self)._deserialize(value, attr, data)

        if self.strip:
            value = value.strip()

        return value
# Maybe alias is better
Str = String


class Schema(_Schema):
    """Schema data always sort, and raise ValidatorError strictly """

    def __init__(self, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)

    class Meta(_Schema.Meta):
        ordered = True
        strict = True


class NotEmpty(Validator):
    """Not Empty Validator"""

    def __call__(self, value):
        if len(value) == 0:
            raise ValidationError('Must not be empty.')
