#!/usr/bin/env python3
"""
Main numbers map
"""
from filepath import FilePath
from filepath import eval_file


class Numbers(dict):

    def __init__(self, *arg, **kw):
        super(Numbers, self).__init__(*arg, **kw)

    @property
    def get_numbers_path(self):
        return FilePath().get_numbers

    @classmethod
    def get_numbers_map(cls):
        number_file = cls().get_numbers_path
        return eval_file(number_file)


print(Numbers.get_numbers_map())
print(Numbers.get_numbers_map()[40])
