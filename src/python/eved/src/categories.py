#!/usr/bin/env python3
# https://codebeautify.org/python-formatter-beautifier
import random
import json
import inspect
import os

from filepath import FilePath
from filepath import eval_file

CATEGORY_ROOT = os.path.dirname(os.path.realpath(__file__))
JSON_ROOT = os.path.join(CATEGORY_ROOT, 'json')

__all__ = [CONTROL_FREAK, HOMOPHOBIC,
           JEALOUS, UNFORGIVING,
           UNJUST, BLOODTHIRSTY
           ]


# HELPERS
def get_all_categories():
    """
    Retrun a list of all categories

    Returns:
        list: ..of Category objects

    """
    cats = list()
    for _category in __all__:
        cats.append(Category(_category['name']))
    return cats


def __create_all_jsons():
    """
    Creates ALL the jsons files for all categories

    """
    for cat in all_categories():
        cat._Category__print_json()


def _create_json(name, data):
    """
    Creates the actual json file
    Uses global JSON_ROOT to find json's location

    Args:
        name (type): name of the file
        data (dict): The dict you want to print into the json

    Returns:
        type: description

    """
    if not os.path.exists(JSON_ROOT):
        os.mkdir(JSON_ROOT)
    json_file = os.path.join(JSON_ROOT, f'{name}.json')
    with open(json_file, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    return json_file


# The CLASS
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
            raise ValueError(f'Could not find given category: {category}')

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

    def __print_json(self):
        """
        Create a json file put of the category's python dict(self)
        """
        return _create_json(self.category, self)
