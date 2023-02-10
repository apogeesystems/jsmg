import jsmg.exceptions as ex

from ._boolean import gen_boolean_cls
from ._integer import gen_integer_cls
from ._number import gen_number_cls
from ._string import gen_string_cls
from ._null import gen_null_cls
from ._array import gen_array_cls

GEN_TYPES = {
    'integer': gen_integer_cls,
    'number': gen_number_cls,
    'string': gen_string_cls,
    'boolean': gen_boolean_cls,
    'null': gen_null_cls,
    'array': gen_array_cls,
}


def from_schema(schema):
    if schema.get('type') is None and schema.get('enum') is None:
        raise ex.UndefinedSchemaTypeException()
    if schema.get('type') == 'array':
        return GEN_TYPES[schema.get('type')](schema, from_schema)
    return GEN_TYPES[schema.get('type')](schema)
