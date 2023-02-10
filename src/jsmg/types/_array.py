import pyrsistent as pyr
import typing
import warnings
import jsmg.exceptions as ex
from ._metadata import gen_metadata_cls
from jsmg._constants import validate_schema_for_type, SchemaType
from jsmg.types import thaw
import json
from itertools import chain


def validate_array_schema(schema):
    validate_schema_for_type(SchemaType.ARRAY, schema)
    if schema.get('prefixItems') or schema.get('items'):
        return
    else:
        raise ex.InvalidArraySchemaException()


def _gen_array_value_properties(schema, props, item_cls=None):
    unique = schema.get('uniqueItems', False)
    meta_cls = gen_metadata_cls(schema)

    def _new(cls, *args):
        self = super(meta_cls, cls).__new__(cls)
        super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
        if args and len(args) > 0:
            for idx in range(len(args)):
                if idx < len(props.keys()):
                    self.__setattr__(list(props.keys())[idx], list(props.values())[idx](args[idx]))
                elif item_cls is None:
                    warnings.warn('Extra argument provided for array item initialization, ignoring...')
                elif unique:  # _additional is pset
                    self._additional = self._additional.add(args[idx])
                else:  # additional is pvector
                    self._additional = self._additional.append(args[idx])
        super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
        return self

    def _repr(self):
        data = []
        for key in props.keys():
            v = self.__getattribute__(key)
            if hasattr(v, 'toJson'):
                data.append(v.toJson())
            elif isinstance(v, set):
                data.append(list(v))
            else:
                data.append(v)
        if self._additional:
            for obj in self._additional:
                if hasattr(obj, 'toJson'):
                    data.append(obj.toJson)
                elif isinstance(obj, set):
                    data.append(list(obj))
                else:
                    data.append(obj)
        return json.dumps(data, indent=2)

    @thaw
    def _setitem(self, key, value):
        if not isinstance(key, int):
            raise TypeError('Invalid key type, key must be an index of type `int`')
        if key < len(props.keys()):
            self.__setattr__(list(props.keys())[key], list(props.values())[key](value))
        elif self._additional and (key - len(props.keys())) <= len(self._additional):
            if item_cls and not isinstance(item_cls, bool):
                if unique:
                    self._additional = self._additional.add(item_cls(value))
                else:
                    self._additional = self._additional.set((key - len(props.keys())), item_cls(value))
            else:
                if unique:
                    if issubclass(type(value), (set, list)) or isinstance(type(value), (set, list)):
                        self._additional = self._additional.add(tuple(value))
                    else:
                        self._additional = self._additional.add(value)
                else:
                    self._additional = self._additional.set((key - len(props.keys())), value)
        else:
            raise IndexError('List index out of range')

    def _getitem(self, key):
        if not isinstance(key, int):
            raise TypeError('Invalid key type, key must be an index of type `int`')
        if key < len(props.keys()):
            return self.__getattribute__(list(props.keys())[key])
        elif self._additional and (key - len(props.keys())) <= len(self._additional):
            return self._additional[key - len(props.keys())]
        else:
            raise IndexError('List index out of range')

    @thaw
    def _delitem(self, key):
        if not isinstance(key, int):
            raise TypeError('Invalid key type, key must be an index of type `int`')
        if key < len(props.keys()):
            self.__setattr__(list(props.keys())[key], list(props.values())[key](None))
        elif self._additional and (key - len(props.keys())) <= len(self._additional):
            self._additional = self._additional.delete(key - len(props.keys()))
        else:
            raise IndexError('List index out of range')

    def _iter(self):
        if not self._additional or len(self._additional) < 1:
            return iter([self.__getattribute__(key) for key in props.keys()])
        return chain(
            iter([self.__getattribute__(key) for key in props.keys()]),
            iter(self._additional),
        )

    def _toJson(self):
        return json.dumps([v for v in self])

    def _hash(self):
        return hash([v for v in self])

    def _get(self, instance, owner):
        for v in self:
            if v is not None:
                return [v for v in self]
        return []

    @thaw
    def _append(self, value):
        idx = -1
        for v in self:
            idx += 1
            if v is not None:
                break
        if idx < len(props.keys()):
            self.__value__.__setattr__(list(props.keys())[idx], list(props.values())[idx](value))

    return {
               **dict([(prop_name, pyr.field(type=klass, initial=klass())) for prop_name, klass in props.items()]),
               '_additional': pyr.field(type=type(None), initial=None) if not item_cls else (
                   pyr.pset_field(item_type=item_cls) if not isinstance(item_cls, bool) and unique else
                   pyr.pvector_field(item_type=item_cls) if not isinstance(item_cls, bool) and not unique else
                   pyr.pset_field(item_type=object) if isinstance(item_cls, bool) and unique else
                   pyr.pvector_field(item_type=object) if isinstance(item_cls, bool) and not unique else
                   None
               ),
               '__new__': _new,
               **dict([
                          ('__setitem__', _setitem),
                          ('__getitem__', _getitem),
                          ('__delitem__', _delitem),
                      ] if not unique else [

               ]),
               '__iter__': _iter,
               'toJson': _toJson,
               '__repr__': _repr,
               '__hash__': _hash,
               '__get__': _get,
           }, meta_cls


def gen_array_value_cls(schema, from_schema):
    prefix_items = schema.get('prefixItems')
    if prefix_items and isinstance(prefix_items, (list, set, tuple)):
        prop_cls = {}
        for idx in range(len(prefix_items)):
            prop_name = prefix_items[idx].get('title', f'_{idx}')
            if prop_name == f'_{idx}':
                warnings.warn(
                    f'Property name (i.e. schema `title`) not set for tuple, property will be named `{prop_name}`')
            prop_cls[prop_name] = from_schema(prefix_items[idx])
        additional_items = schema.get('additionalItems')
        items = schema.get('items')
        items_cls = None
        if additional_items and isinstance(additional_items, (dict, bool)):
            if items:
                warnings.warn(
                    'Both `items` and `additionalItems` properties are set, defaulting to using `additionalItems`')
            if isinstance(additional_items, dict):
                items_cls = from_schema(additional_items)
            else:
                item_cls = additional_items
        elif additional_items and not isinstance(additional_items, (dict, bool)):
            raise ex.InvalidAdditionalItemsTypeException(additional_items)
        elif items and isinstance(items, (dict, bool)):
            if isinstance(items, dict):
                items_cls = from_schema(items)
            else:
                items_cls = items
        elif items and not isinstance(items, (dict, bool)):
            raise ex.InvalidItemsTypeException(items)
        props, meta_cls = _gen_array_value_properties(schema, prop_cls, items_cls)
        return type(
            f'_ArrayValueType_{id(schema)}',
            (meta_cls,),
            props,
        )
    elif prefix_items and not isinstance(prefix_items, (list, set, tuple)):
        raise ex.InvalidPrefixItemsTypeException(prefix_items)


def gen_array_field(schema, from_schema):
    value_cls = gen_array_value_cls(schema, from_schema)
    if value_cls:
        return value_cls, pyr.field(type=value_cls, initial=value_cls()), value_cls
    klass = from_schema(schema.get('items'))
    initial = []
    if schema.get('default'):
        for item in schema.get('default'):
            initial.append(klass(item))
    if schema.get('uniqueItems'):
        return pyr.pset, pyr.pset_field(item_type=klass, initial=initial), klass
    return pyr.pvector, pyr.pvector_field(item_type=klass, initial=initial), klass


def gen_array_metadata_cls(schema):
    class _ArrayMetadata(gen_metadata_cls(schema)):
        items: typing.ClassVar[typing.Optional[typing.Union[dict, bool]]] = pyr.field(type=pyr.optional(dict, bool),
                                                                                      initial=schema.get('items'))
        additionalItems: typing.ClassVar[typing.Optional[typing.Union[dict, bool]]] = pyr.field(
            type=pyr.optional(dict, bool), initial=schema.get('additionalItems'))
        prefixItems: typing.ClassVar[typing.Optional[list]] = pyr.field(type=pyr.optional(list),
                                                                        initial=schema.get('prefixItems'))
        contains: typing.ClassVar[typing.Optional[dict]] = pyr.field(type=pyr.optional(dict),
                                                                     initial=schema.get('contains'))
        minContains: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                       initial=schema.get('minContains'),
                                                                       invariant=lambda x: (x is None or x >= 0,
                                                                                            'minContains must be a non-negative integer'))
        maxContains: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                       initial=schema.get('maxContains'),
                                                                       invariant=lambda x: (x is None or x >= 0,
                                                                                            'maxContains must be a non-negative integer'))
        minItems: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                    initial=schema.get('minItems'),
                                                                    invariant=lambda x: (
                                                                        x is None or x >= 0,
                                                                        'minItems must be a non-negative integer'))
        maxItems: typing.ClassVar[typing.Optional[int]] = pyr.field(type=pyr.optional(int),
                                                                    initial=schema.get('maxItems'),
                                                                    invariant=lambda x: (
                                                                        x is None or x >= 0,
                                                                        'maxItems must be a non-negative integer'))
        uniqueItems: typing.ClassVar[typing.Optional[bool]] = pyr.field(type=pyr.optional(bool),
                                                                        initial=schema.get('uniqueItems'))

        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

    return _ArrayMetadata


def gen_array_cls(schema, from_schema):
    validate_array_schema(schema)

    typ, field, klass = gen_array_field(schema, from_schema)

    class _Array(gen_array_metadata_cls(schema)):
        __value__: typing.Optional[typ] = field

        def __new__(cls, *args, **kwargs):
            self = super().__new__(cls)
            if len(args) > 0:
                super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
                if klass.__name__.startswith('_ArrayValueType'):
                    self.__value__ = klass(*args)
                else:
                    for arg in args:
                        if typ == pyr.pvector:
                            if isinstance(arg, (list, set, tuple)):
                                self.__value__ = self.__value__.append(klass(*arg))
                            else:
                                self.__value__ = self.__value__.append(klass(arg))
                        elif typ == pyr.pset:
                            if isinstance(arg, (list, set, tuple)):
                                self.__value__ = self.__value__.add(klass(*arg))
                            else:
                                self.__value__ = self.__value__.add(klass(arg))

                super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
            return self

        def __get__(self, instance, owner):
            return self.__value__

        @thaw
        def __set__(self, instance, iterable):
            self.__value__ = [klass(v) for v in iterable]

        def __repr__(self):
            if klass.__name__.startswith('_ArrayValueType'):
                return self.__value__.__repr__() if self.__value__ is not None else str(None)
            if typ == pyr.pvector:
                return json.dumps(self.__value__.tolist(), indent=2, default=lambda o: o.toJson())
            elif typ == pyr.pset:
                return json.dumps([v for v in self.__value__], indent=2, default=lambda o: o.toJson())

        def toJson(self):
            return [v.toJson() if hasattr(v, 'toJson') else v for v in self.__value__.tolist()]

        def __hash__(self):
            return hash(self.__value__)

        def __len__(self):
            return self.__value__.__len__()

        def __getitem__(self, key):
            if typ == pyr.pset:
                raise TypeError('`set` object is not subscriptable')
            elif not isinstance(key, int):
                raise TypeError('Invalid key type, key must be an index of type `int`')
            return self.__value__[key]

        @thaw
        def __setitem__(self, key, value):
            if typ == pyr.pset:
                raise TypeError('`set` object is not subscriptable')
            elif not isinstance(key, int):
                raise TypeError('Invalid key type, key must be an index of type `int`')
            elif self.__value__.__class__.__name__.startswith('_ArrayValueType'):
                self.__value__[key] = value
            elif typ == pyr.pvector:
                self.__value__ = self.__value__.set(key, klass(value))
            else:
                raise TypeError(f'Unhandled field type `{typ.__name__}`')

        @thaw
        def __delitem__(self, key):
            if typ == pyr.pset:
                raise TypeError('`set` object is not subscriptable')
            elif not isinstance(key, int):
                raise TypeError('Invalid key type, key must be an index of type `int`')
            if self.__value__.__class__.__name__.startswith('_ArrayValueType') or typ == pyr.pvector:
                del self.__value__[key]
            else:
                raise TypeError(f'Unhandled field type `{typ.__name__}`')

        def __iter__(self):
            return self.__value__.__iter__()

        def __reversed__(self):
            if typ == pyr.pset:
                warnings.warn('`set` object is not reversible, returning current set')
                return self.__value__
            return reversed(self.__value__)

        def __contains__(self, value):
            return value in self.__value__

        @thaw
        def add(self, value):
            if typ == pyr.pvector:
                raise AttributeError('`list` object has no attribute `add` (use `append`)')
            self.__value__ = self.__value__.add(klass(value))

        @thaw
        def update(self, iterable):
            if typ == pyr.pvector:
                raise AttributeError('`list` object has no attribute `update` (use `extend`)')
            self.__value__ = self.__value__.update([klass(v) for v in iterable])

        @thaw
        def remove(self, value):
            if typ == pyr.pvector:
                raise AttributeError('`list` object has no attribute `remove` (use `del _Array[<index>]`)')
            self.__value__ = self.__value__.remove(klass(value))

        @thaw
        def append(self, value):
            if typ == pyr.pset:
                raise AttributeError('`set` object has no attribute `append` (use `add`)')
            self.__value__ = self.__value__.append(klass(value))

        @thaw
        def extend(self, iterable):
            if typ == pyr.pset:
                raise AttributeError('`set` object has no attribute `extend` (use `update`)')
            self.__value__ = self.__value__.extend([klass(v) for v in iterable])

    return _Array
