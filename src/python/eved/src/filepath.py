#!/usr/bin/env python3
"""
Main area to know where all the files are
"""
import os
import inspect
import json
from sys import platform

APP_ROOT_FOLDER = os.path.realpath(__file__)
APP_ROOT_FOLDER = os.path.dirname(APP_ROOT_FOLDER)
APP_ROOT_FOLDER = os.path.dirname(APP_ROOT_FOLDER)
DATA_FOLDER = 'data'
TESTS_FOLDER = 'tests'
CATEGORIES_FOLDER = 'categories'
CATEGORIES_TYPE_PYTHON = 'python'
CATEGORIES_TYPE_JSON = 'json'
NUMBERS_FOLDER = 'numbers'
BOOKS_FOLDER = 'books'


def eval_file(filepath):
    return eval(open(filepath, 'r', encoding="utf8").read())


def create_all_jsons():
    """
    This will create each python category and make a json out of it

    Return:
        (list): of json filepaths
    """
    jsons = list()

    pyhon_root = FilePath().get_categories_python
    if not os.path.exists(pyhon_root):
        raise IOError('Python categories folder not found!')

    for file in os.listdir(pyhon_root):
        data = eval_file(os.path.join(pyhon_root, file))
        _create_json(os.path.join(pyhon_root, file), data)


def _create_json(filepath, data):
    """
    Creates the actual json file from given pathon dict file

    Args:
        filepath (type): name of the file python file
        data (dict): The dict you want to print into the json

    Returns:
        type: description

    """
    json_root = FilePath().get_categories_json
    if not os.path.exists(json_root):
        raise IOError('Json categories folder not found!')

    json_basename = os.path.basename(filepath).split('.')[0]
    json_file = os.path.join(json_root, f'{json_basename}.json')
    with open(json_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return json_file


r"""
  ____| _)  |         _ \         |    |           ___|  |
  |      |  |   _ \  |   |  _` |  __|  __ \       |      |   _` |   __|   __|
  __|    |  |   __/  ___/  (   |  |    | | |      |      |  (   | \__ \ \__ \
 _|     _| _| \___| _|    \__,_| \__| _| |_|     \____| _| \__,_| ____/ ____/
"""


class FilePath(object):
    """
    Takes care of files system stuff
    """
    def __init__(self):
        self.root = APP_ROOT_FOLDER

    @property
    def get_root(self):
        return self.root

    @property
    def get_data(self):
        data = os.path.join(self.root, DATA_FOLDER)
        if os.path.exists(data):
            return data
        raise ValueError('Missing data folder!')

    @property
    def get_tests(self):
        tests = os.path.join(self.root, TESTS_FOLDER)
        if os.path.exists(tests):
            return tests
        raise ValueError('Missing tests folder!')

    @property
    def get_caterogies(self):
        return os.path.join(self.get_data, CATEGORIES_FOLDER)

    @property
    def get_categories_python(self):
        return os.path.join(self.get_caterogies, CATEGORIES_TYPE_PYTHON)

    @property
    def get_categories_json(self):
        return os.path.join(self.get_caterogies, CATEGORIES_TYPE_JSON)

    @property
    def get_books(self):
        return os.path.join(self.get_data, BOOKS_FOLDER, 'map.py')

    @property
    def get_numbers(self):
        return os.path.join(self.get_data, NUMBERS_FOLDER, 'map.py')


# d = FilePath()
# print('cat    ', d.get_caterogies)
# print('python.', d.get_categories_python)
# create_all_jsons()
