import jsmg._utilities as utils


class InvalidSchemaTypeException(TypeError):
    def __init__(self, schema, *args, expected=None, **kwargs):
        if not expected:
            super().__init__(
                f'Invalid schema type definition `{schema.get("type")}`, expected one of {", ".join(["`" + typ + "`" for typ in utils.valid_types()])}'
            )
        else:
            super().__init__(
                f'Invalid schema type definition `{schema.get("type")}`, expected `{expected}`'
            )


class UndefinedSchemaTypeException(AttributeError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            f'Undefined schema type one of {", ".join(["`" + typ + "`" for typ in utils.valid_types()])} must be provided otherwise enum must be defined'
        )


class InvalidPrefixItemsTypeException(TypeError):
    def __init__(self, prefix_items, *args, **kwargs):
        super().__init__(
            f'Invalid prefixItems type `{type(prefix_items).__name__}`, expecting one of `list`, `set` or `tuple`'
        )


class InvalidAdditionalItemsTypeException(TypeError):
    def __init__(self, additional_items, *args, **kwargs):
        super().__init__(
            f'Invalid prefixItems type `{type(additional_items).__name__}`, expecting one of `bool` or `dict`'
        )


class InvalidArraySchemaException(AttributeError):
    def __init__(self):
        super().__init__(
            'Invalid array schema, at least one of `prefixItems` or `items` fields must be defined'
        )


InvalidItemsTypeException = InvalidAdditionalItemsTypeException
