from jsmg.types import *
from itertools import chain
# from jsmg._utilities import from_schema
import json
import types
import inspect

t = from_schema({
    'type': 'array',
    'prefixItems': [
        {'type': 'string', 'title': 'the_title'},
        {'type': 'integer', 'title': 'the_index'},
    ],
    'items': False,
    # 'uniqueItems': True,
})
u = from_schema({
    'type': 'array',
    'items': {
        'type': 'array',
        'items': {'type': 'integer'}
    },
    'uniqueItems': True
})
# t = from_schema({'type': 'string', 'default': 'asdf'})
# print(json.dumps(dir(t), indent=2))
# print(t._pclass_fields['default'].initial) # Get default for class
# a = t(5.0)
a = t('2', 1)
# a.append('asdf')
print(a)
# a = t(None, 10, True, [])
# a[0] = "1"
# a[1] = 2
# a[2] = True
# a[3] = False
# a[4] = None
# print(a)
# for item in a:
#     print(item)
# print(json.dumps(t.metadata(), indent=2))
b = u([1, 2], [3, 4], {1, 2}, (4,5))
# print(b)
# b = u('hello', 'world', '?', '1')
# print(b)
# b.add('asdf')
# b.remove('hello')
# b.update(['a','b'])
# b.add(['c','d'])
# print(b)
# print('world' in b)
# b[0] = 'hello'
# b[1] = 'world'
# b[2] = '!'
# b[3] = None
# print(json.dumps(u.metadata(), indent=2))
# print(json.dumps(b.metadata(), indent=2))
# for item in b:
#     print(item)


# class MyNumbers:
#     aa = {'a': 1, 'b': 10}
#     bb = [2, 3, 4]
#
#     def __iter__(self):
#         return chain(iter(self.aa.values()), iter(self.bb))
#         # self._idx = 0
#         # return self
#
#     # def __next__(self):
#     #     if self._idx < len(list(self.aa.keys())):
#     #         x = list(self.aa.values())[self._idx]
#     #         self._idx += 1
#     #         return x
#     #     x = self.bb[self._idx - len(list(self.aa.keys()))]
#     #     self._idx += 1
#     #     return x
#
#
# myclass = MyNumbers()
# for a in myclass:
#     print(a)
# # myiter = iter(myclass)
# #
# # print(next(myiter))
# # print(next(myiter))
# # print(next(myiter))
# # print(next(myiter))
# # print(next(myiter))
