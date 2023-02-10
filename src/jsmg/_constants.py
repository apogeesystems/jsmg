import pyrsistent as pyr
from enum import Enum
import jsmg.exceptions as ex

EMPTY = object()

DEFAULT_TYPES = {'integer', 'number', 'string', 'null', 'object', 'array', 'boolean'}

DEFAULT_TYPING = {
    'integer': pyr.optional(int),
    'number': pyr.optional(int, float),
    'string': pyr.optional(str),
    'null': type(None),
    'object': pyr.optional(dict),
    'array': pyr.optional(list, set, tuple),
    'boolean': pyr.optional(bool),
}


class SchemaType(Enum):
    INTEGER = 'integer'
    NUMBER = 'number'
    STRING = 'string'
    NULL = 'null'
    OBJECT = 'object'
    ARRAY = 'array'
    BOOLEAN = 'boolean'


def validate_schema_for_type(typ, schema):
    if type(typ) == SchemaType:
        typ = typ.value
    if schema.get('type') is None:
        raise ex.UndefinedSchemaTypeException()
    elif schema.get('type') != typ:
        raise ex.InvalidSchemaTypeException(schema, expected=typ)
