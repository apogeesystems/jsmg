import pyrsistent as pyr
import typing
from jsmg._constants import SchemaType, EMPTY, validate_schema_for_type
from ._metadata import gen_metadata_cls, gen_default_type
from jsmg.types import thaw


def number_value_invariant(value):
    return isinstance(value, pyr.optional(float)) and not isinstance(value,
                                                                     bool), f'Invalid value type `{type(value).__name__}`, expected `int` or `float`'


def gen_number_metadata_cls(schema):
    typing_cls = int if schema.get('type') == 'integer' else float

    class _NumberMetadata(gen_metadata_cls(schema)):
        multipleOf: typing.ClassVar[typing.Optional[typing_cls]] = pyr.field(
            type=gen_default_type(schema), initial=schema.get('multipleOf'))
        minimum: typing.ClassVar[typing.Optional[typing_cls]] = pyr.field(
            type=gen_default_type(schema), initial=schema.get('minimum'))
        exclusiveMinimum: typing.ClassVar[typing.Optional[
            typing.Union[typing_cls, bool]]] = pyr.field(
            type=gen_default_type(schema) + (bool,),
            initial=schema.get('exclusiveMinimum'))
        maximum: typing.ClassVar[typing.Optional[typing_cls]] = pyr.field(
            type=gen_default_type(schema),
            initial=schema.get('maximum'))
        exclusiveMaximum: typing.ClassVar[typing.Optional[
            typing.Union[typing_cls, bool]]] = pyr.field(
            type=gen_default_type(schema) + (bool,),
            initial=schema.get('exclusiveMaximum'))

        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

    return _NumberMetadata


def gen_number_cls(schema):
    validate_schema_for_type(SchemaType.NUMBER, schema)

    class _Number(gen_number_metadata_cls(schema)):
        __value__: typing.Optional[float] = pyr.field(type=pyr.optional(float), initial=schema.get('default'),
                                                      invariant=number_value_invariant)

        def __new__(cls, value: typing.Optional[typing.Union[int, float]] = EMPTY, *args, **kwargs):
            self = super().__new__(cls)
            if value != EMPTY:
                if not isinstance(value, pyr.optional(int, float)):
                    raise TypeError(
                        f'Invalid value type `{type(value).__name__}`, expected one of `int`, `float` or `NoneType`')
                super(pyr.PClass, self).__setattr__('_pclass_frozen', False)
                self.__value__ = float(value) if value is not None else None
                super(pyr.PClass, self).__setattr__('_pclass_frozen', True)
            return self

        def __get__(self, instance, owner):
            return self.__value__

        @thaw
        def __set__(self, instance, value: typing.Optional[typing.Union[int, float]]):
            self.__value__ = float(value) if value is not None else None

        def __repr__(self):
            return self.__value__

        def toJson(self):
            return self.__value__

        def __hash__(self):
            return hash(self.__value__)

        def __eq__(self, other):
            if isinstance(other, _Number) or hasattr(other, '__value__'):
                return self.__value__ == other.__value__
            return self.__value__ == other

        def __ne__(self, other):
            if isinstance(other, _Number) or hasattr(other, '__value__'):
                return self.__value__ != other.__value__
            return self.__value__ != other

        def __lt__(self, other):
            if isinstance(other, _Number) or hasattr(other, '__value__'):
                return self.__value__ < other.__value__
            return self.__value__ < other

        def __gt__(self, other):
            if isinstance(other, _Number) or hasattr(other, '__value__'):
                return self.__value__ > other.__value__
            return self.__value__ > other

        def __le__(self, other):
            return self.__lt__(other) or self.__eq__(other)

        def __ge__(self, other):
            return self.__gt__(other) or self.__eq__(other)

        def __pos__(self):
            return self.__value__.__pos__()

        def __neg__(self):
            return self.__value__.__neg__()

        def __abs__(self):
            return self.__value__.__abs__()

        def __round__(self, n=None):
            return self.__value__.__round__(n)

        def __floor__(self):
            return self.__value__.__floor__()

        def __ceil__(self):
            return self.__value__.__ceil__()

        def __trunc__(self):
            return self.__value__.__trunc__()

        def __add__(self, other):
            return self.__value__.__add__(other)

        def __radd__(self, other):
            return self.__add__(other)

        @thaw
        def __iadd__(self, other):
            self.__value__ = self.__add__(other)
            return self

        def __sub__(self, other):
            return self.__value__.__sub__(other)

        def __rsub__(self, other):
            return other.__sub__(self.__value__)

        @thaw
        def __isub__(self, other):
            self.__value__ = self.__sub__(other)
            return self

        def __mul__(self, other):
            return self.__value__.__mul__(other)

        def __rmul__(self, other):
            return self.__mul__(other)

        @thaw
        def __imul__(self, other):
            self.__value__ = self.__mul__(other)
            return self

        def __floordiv__(self, other):
            return self.__value__.__floordiv__(other)

        def __rfloordiv__(self, other):
            return other.__floordiv__(self.__value__)

        @thaw
        def __ifloordiv__(self, other):
            self.__value__ = self.__floordiv__(other)
            return self

        def __truediv__(self, other):
            return self.__value__.__truediv__(other)

        def __rtruediv__(self, other):
            return other.__truediv__(self.__value__)

        @thaw
        def __itruediv__(self, other):
            self.__value__ = self.__truediv__(other)
            return self

        @thaw
        def __idiv__(self, other):
            self.__value__ = self.__truediv__(other)
            return self

        def __mod__(self, other):
            return self.__value__.__mod__(other)

        def __rmod__(self, other):
            return other.__mod__(self.__value__)

        @thaw
        def __imod__(self, other):
            self.__value__ = self.__mod__(other)
            return self

        def __divmod__(self, other):
            return self.__value__.__divmod__(other)

        def __rdivmod__(self, other):
            return other.__divmod__(self.__value__)

        def __pow__(self, power, modulo=None):
            return self.__value__.__pow__(power, modulo)

        def __rpow__(self, other, modulo=None):
            return other.__pow__(self.__value__, modulo)

        @thaw
        def __ipow__(self, other, modulo=None):
            self.__value__ = self.__pow__(other, modulo)
            return self

        def __rlshift__(self, other):
            return other.__lshift__(self.__value__)

        @thaw
        def __ilshift__(self, other):
            self.__value__ = self.__lshift__(other)
            return self

        def __rrshift__(self, other):
            return other.__rshift__(self.__value__)

        @thaw
        def __irshift__(self, other):
            self.__value__ = self.__rshift__(other)
            return self

        def __rand__(self, other):
            return other.__and__(self.__value__)

        @thaw
        def __iand__(self, other):
            self.__value__ = self.__and__(other)
            return self

        def __ror__(self, other):
            return other.__or__(self.__value__)

        @thaw
        def __ior__(self, other):
            self.__value__ = self.__or__(other)
            return self

        def __rxor__(self, other):
            return other.__xor__(self.__value__)

        @thaw
        def __ixor__(self, other):
            self.__value__ = self.__xor__(other)
            return self

        def __bool__(self):
            return self.__value__ if self.__value__ is not None else False

        def __int__(self):
            return self.__value__.__int__()

        def __long__(self):
            return self.__value__.__int__()

        def __float__(self):
            return self.__value__.__float__()

        def __complex__(self):
            return complex(self.__value__)

    return _Number
