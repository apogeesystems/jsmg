import pyrsistent as pyr
import typing
import json
from jsmg._constants import DEFAULT_TYPES, DEFAULT_TYPING

_VALID_TYPES = pyr.pset(DEFAULT_TYPES)


def valid_types():
    return _VALID_TYPES


def gen_default_type(schema):
    return DEFAULT_TYPING.get(schema.get('type'))


def schema_type_invariant(value):
    return value in valid_types(), f'Invalid schema type `{value}` expected one of {", ".join(["`" + typ + "`" for typ in valid_types()])}'


def gen_metadata_cls(schema, bases=(pyr.PClass,)):
    class _Metadata(*bases):
        _schema: typing.ClassVar[dict] = pyr.field(type=dict, initial=schema, mandatory=True)
        type: typing.ClassVar[str] = pyr.field(type=str, initial=schema.get('type'),
                                               invariant=schema_type_invariant)
        title: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str), initial=schema.get('title'))
        description: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str),
                                                                       initial=schema.get('description'))
        default: typing.ClassVar[typing.Optional[typing.Any]] = pyr.field(
            type=gen_default_type(schema), initial=schema.get('default'))
        examples: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list),
                                                                     initial=schema.get('examples'))
        readOnly: typing.ClassVar[typing.Optional[bool]] = pyr.field(type=pyr.optional(bool),
                                                                     initial=schema.get('readOnly'))
        writeOnly: typing.ClassVar[typing.Optional[bool]] = pyr.field(type=pyr.optional(bool),
                                                                      initial=schema.get('writeOnly'))
        deprecated: typing.ClassVar[typing.Optional[bool]] = pyr.field(type=pyr.optional(bool),
                                                                       initial=schema.get('deprecated'))
        comment: typing.ClassVar[typing.Optional[str]] = pyr.field(type=pyr.optional(str),
                                                                   initial=schema.get('$comment'))
        enum: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list), initial=schema.get('enum'))
        anyOf: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list), initial=schema.get('anyOf'))
        allOf: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list), initial=schema.get('allOf'))
        oneOf: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list), initial=schema.get('onOf'))
        not_: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list), initial=schema.get('not'))

        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

        def __repr__(self):
            d = self._to_dict()
            del d['_schema']
            if hasattr(self, '__value__'):
                del d['__value__']
            return json.dumps(d, indent=2)

        @classmethod
        def metadata(cls, full=False):
            inst = cls.create({})
            return dict(
                [(key, value) for key, value in inst._to_dict().items() if key != '_schema' and key != '__value__' and (value is not None or full)]
            )

    return _Metadata
