#!/usr/bin/env python3
import os

from filepath import FilePath
from filepath import eval_file

# Load every .py file from data/categories/python/ into __all__ at import time
_python_root = FilePath().get_categories_python
__all__ = [
    eval_file(os.path.join(_python_root, f))
    for f in sorted(os.listdir(_python_root))
    if f.endswith('.py')
]


def get_all_categories():
    """Return a list of all Category objects."""
    return [Category(c['name']) for c in __all__]


def category_names():
    """Return a sorted list of all category name strings."""
    return [c['name'] for c in __all__]


class Category(dict):
    TYPE = None

    def __init__(self, category, is_true=False):
        self.category = None
        self.is_true = is_true
        for _category in __all__:
            if _category['name'] == category:
                super(Category, self).__init__(_category)
                self.category = category
        if not self.category:
            raise ValueError(
                f'Could not find category: {category!r}. '
                f'Available: {category_names()}'
            )

    def __repr__(self):
        return f'{self.__class__.__name__}({self.category})'

    def __str__(self):
        return self['nice_name']

    @property
    def true(self):
        return self.is_true

    @true.setter
    def true(self, true):
        self.is_true = true

    @classmethod
    def create(cls, category):
        return cls(category)

    def to_json(self):
        """Write this category to its JSON file and return the path."""
        from filepath import _create_json
        py_file = os.path.join(FilePath().get_categories_python, f'{self.category}.py')
        return _create_json(py_file, dict(self))
