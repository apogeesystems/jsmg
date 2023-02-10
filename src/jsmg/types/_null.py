from jsmg._constants import validate_schema_for_type, SchemaType
from ._metadata import gen_metadata_cls
import json


def gen_null_cls(schema):
    validate_schema_for_type(SchemaType.NULL, schema)

    class _Null(gen_metadata_cls(schema)):
        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

        def __get__(self, instance, owner) -> None:
            return None

        def __repr__(self) -> str:
            return str(None)

        def toJson(self) -> str:
            return json.dumps(None)

    return _Null
