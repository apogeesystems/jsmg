import pyrsistent as pyr
import typing
from jsmg._constants import EMPTY, validate_schema_for_type, SchemaType
from ._metadata import gen_metadata_cls
from jsmg.types import thaw
import json


def string_value_invariant(value):
    return isinstance(value, pyr.optional(str)) and not isinstance(value,
                                                                   bool), f'Invalid value type `{type(value).__name__}`, expected `str`'


def gen_string_metadata_cls(schema):
    class _StringMetadata(gen_metadata_cls(schema)):
        minLength: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                     initial=schema.get('minLength'))
        maxLength: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                     initial=schema.get('maxLength'))
        pattern: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str),
                                                                   initial=schema.get('pattern'))
        format_: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str), initial=schema.get('format'))
        contentEncoding: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str),
                                                                           initial=schema.get('contentEncoding'))
        contentMediaType: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str),
                                                                            initial=schema.get('contentMediaType'))

        # contentSchema TODO find out more about contentSchema definitions

        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

    return _StringMetadata


def gen_string_cls(schema):
    validate_schema_for_type(SchemaType.STRING, schema)

    class _String(gen_string_metadata_cls(schema)):
        __value__: typing.Optional[str] = pyr.field(type=pyr.optional(str), initial=schema.get('default'),
                                                    invariant=string_value_invariant)

        def __new__(cls, value: typing.Optional[str] = EMPTY, *args, **kwargs):
            self = super().__new__(cls)
            if value != EMPTY:
                if not isinstance(value, pyr.optional(str)):
                    raise TypeError(f'Invalid value type `{type(value).__name__}`, expected one of `str` or `NoneType`')
                super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
                self.__value__ = value
                super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
            return self

        def __get__(self, instance, owner):
            return self.__value__

        @thaw
        def __set__(self, instance, value: typing.Optional[str]):
            self.__value__ = value

        def __repr__(self):
            return self.__value__

        def toJson(self):
            return self.__value__

        def __hash__(self):
            return hash(self.__value__)

        def __eq__(self, other):
            if isinstance(other, _String) or hasattr(other, '__value__'):
                return self.__value__ == other.__value__
            return self.__value__ == other

        def __ne__(self, other):
            if isinstance(other, _String) or hasattr(other, '__value__'):
                return self.__value__ != other.__value__
            return self.__value__ != other

        def __lt__(self, other):
            if isinstance(other, _String) or hasattr(other, '__value__'):
                return self.__value__ < other.__value__
            return self.__value__ < other

        def __gt__(self, other):
            if isinstance(other, _String) or hasattr(other, '__value__'):
                return self.__value__ > other.__value__
            return self.__value__ > other

        def __le__(self, other):
            return self.__lt__(other) or self.__eq__(other)

        def __ge__(self, other):
            return self.__gt__(other) or self.__eq__(other)

        def __len__(self):
            return self.__value__.__len__()

        def __getitem__(self, key):
            return self.__value__.__getitem__(key)

        def __iter__(self):
            return self.__value__.__iter__()

        def __reversed__(self):
            return self.__value__.__reversed__()

        def __contains__(self, item):
            return self.__value__.__contains__(item)

        def capitalize(self):
            return self.__value__.capitalize()

        def casefold(self):
            return self.__value__.casefold()

        def center(self, width, fillchar=' '):
            return self.__value__.center(width, fillchar)

        def count(self, sub, start=None, end=None):
            return self.__value__.count(sub, start, end)

        def encode(self, encoding='utf-8', errors='strict'):
            return self.__value__.encode(encoding, errors)

        def endswith(self, suffix, start=None, end=None):
            return self.__value__.endswith(suffix, start, end)

        def expandtabs(self, tabsize=8):
            return self.__value__.expandtabs(tabsize)

        def find(self, sub, start=None, end=None):
            return self.__value__.find(sub, start, end)

        def format(self, *args, **kwargs):
            return self.__value__.format(args, kwargs)

        def format_map(self, **mapping):
            return self.__value__.format_map(mapping)

        def index(self, sub, start=None, end=None):
            return self.__value__.index(sub, start, end)

        def isalnum(self):
            return self.__value__.isalnum()

        def isalpha(self):
            return self.__value__.isalpha()

        def isascii(self):
            return self.__value__.isascii()

        def isdecimal(self):
            return self.__value__.isdecimal()

        def isdigit(self):
            return self.__value__.isdigit()

        def isidentifier(self):
            return self.__value__.isidentifier()

        def islower(self):
            return self.__value__.islower()

        def isnumberic(self):
            return self.__value__.isnumeric()

        def isprintable(self):
            return self.__value__.isprintable()

        def isspace(self):
            return self.__value__.isspace()

        def istitle(self):
            return self.__value__.istitle()

        def isupper(self):
            return self.__value__.isupper()

        def join(self, *args):
            return self.__value__.join(args)

        def ljust(self, width, fillchar=' '):
            return self.__value__.ljust(width, fillchar)

        def lower(self):
            return self.__value__.lower()

        def lstrip(self, chars=None):
            return self.__value__.lstrip(chars)

        def maketrans(self, x, y=None, z=None):
            if y is not None and z is None:
                return self.__value__.maketrans(x, y)
            elif z is not None:
                return self.__value__.maketrans(x, y, z)
            return self.__value__.maketrans(x)

        def partition(self, sep):
            return self.__value__.partition(sep)

        def removeprefix(self, prefix):
            return self.__value__.removeprefix(prefix)

        def removesuffix(self, suffix):
            return self.__value__.removesuffix(suffix)

        def replace(self, old, new, count=-1):
            return self.__value__.replace(old, new, count)

        def rfind(self, sub, start=None, end=None):
            return self.__value__.rfind(sub, start, end)

        def rindex(self, sub, start=None, end=None):
            return self.__value__.rindex(sub, start, end)

        def rjust(self, width, fillchar=' '):
            return self.__value__.rjust(width, fillchar)

        def rpartition(self, sep):
            return self.__value__.rpartition(sep)

        def rsplit(self, sep=None, maxsplit=-1):
            return self.__value__.rsplit(sep, maxsplit)

        def rstrip(self, chars=None):
            return self.__value__.rstrip(chars)

        def split(self, sep=None, maxsplit=-1):
            return self.__value__.split(sep, maxsplit)

        def splitlines(self, keepends=False):
            return self.__value__.splitlines(keepends)

        def startswith(self, prefix, start=None, end=None):
            return self.__value__.startswith(prefix, start, end)

        def strip(self, chars=None):
            return self.__value__.strip(chars)

        def swapcase(self):
            return self.__value__.swapcase()

        def title_(self):
            return self.__value__.title()

        def translate(self, table):
            return self.__value__.translate(table)

        def upper(self):
            return self.__value__.upper()

        def zfill(self, width: int):
            return self.__value__.zfill(width)

    return _String
