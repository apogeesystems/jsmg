# from jsmg.types import *
import pyrsistent as pyr
import typing
from jsmg._constants import EMPTY, validate_schema_for_type
from ._metadata import gen_metadata_cls
from jsmg.types import thaw
import json


def gen_boolean_cls(schema):
    validate_schema_for_type('boolean', schema)

    class _Boolean(gen_metadata_cls(schema)):
        __value__: typing.Optional[bool] = pyr.field(type=pyr.optional(bool), initial=schema.get('default'))

        def __new__(cls, value: typing.Optional[bool] = EMPTY, *args, **kwargs):
            self = super().__new__(cls)
            if value != EMPTY:
                if not isinstance(value, pyr.optional(bool)):
                    raise TypeError(f'Invalid value type `{type(value).__name__}`, expected one of `bool` or `NoneType`')
                super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
                self.__value__ = value
                super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
            return self

        def __get__(self, instance, owner):
            return self.__value__

        @thaw
        def __set__(self, instance, value: typing.Optional[bool]):
            self.__value__ = value

        def __repr__(self):
            return self.__value__.__repr__()

        def toJson(self):
            return self.__value__

        def __eq__(self, other):
            if isinstance(other, _Boolean) or hasattr(other, '__value__'):
                return self.__value__ == other.__value__
            return self.__value__ == other

        def __bool__(self):
            return self.__value__ if self.__value__ is not None else False

    return _Boolean
