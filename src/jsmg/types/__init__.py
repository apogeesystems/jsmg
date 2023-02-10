from __future__ import annotations, division

import pyrsistent as pyr
import typing
import json
import warnings

# import jsmg._utilities as utils
import jsmg._constants as const
import jsmg.exceptions as ex


def thaw(func):
    def wrapper(self, *args, **kwargs):
        super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
        res = func(self, *args, **kwargs)
        super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
        return res

    return wrapper


from ._common import from_schema

# __all__ = [
#     'gen_metadata_cls',
#     'gen_number_metadata_cls',
#     'gen_string_metadata_cls',
#     'gen_array_metadata_cls',
#     'gen_boolean_cls',
#     'gen_integer_cls',
#     'gen_number_cls',
#     'gen_string_cls',
#     'gen_null_cls',
#     'gen_array_cls'
# ]
